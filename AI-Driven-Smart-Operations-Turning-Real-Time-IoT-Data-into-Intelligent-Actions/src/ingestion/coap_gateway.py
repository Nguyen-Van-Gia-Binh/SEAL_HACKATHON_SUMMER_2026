import asyncio
import json
import logging
import time
from kafka import KafkaProducer
from src.config import settings

try:
    import aiocoap
    import aiocoap.resource as resource
    AIOCOAP_AVAILABLE = True
except ImportError:
    AIOCOAP_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (CoAP-Gateway) %(message)s")
logger = logging.getLogger("coap_gateway")

class TelemetryResource(resource.Resource if AIOCOAP_AVAILABLE else object):
    """
    CoAP Resource for receiving sensor readings via POST /telemetry
    """
    def __init__(self, kafka_producer):
        super().__init__()
        self.kafka_producer = kafka_producer

    async def render_post(self, request):
        try:
            payload_str = request.payload.decode("utf-8")
            data = json.loads(payload_str)
            
            station_id = data.get("station_id", "STN_COAP_NODE")
            data["protocol"] = "CoAP"
            data["ingestion_timestamp"] = time.time()
            if "event_time" not in data:
                data["event_time"] = time.time()

            if self.kafka_producer:
                self.kafka_producer.send(
                    settings.TOPIC_RAW,
                    key=station_id,
                    value=data
                )
                logger.debug(f"Bridged CoAP -> Kafka [{settings.TOPIC_RAW}] Station: {station_id}")

            response_payload = json.dumps({"status": "SUCCESS", "received_at": data["ingestion_timestamp"]}).encode("utf-8")
            return aiocoap.Message(code=aiocoap.CHANGED, payload=response_payload)
        except Exception as e:
            logger.error(f"Error in CoAP POST /telemetry: {e}")
            return aiocoap.Message(code=aiocoap.INTERNAL_SERVER_ERROR, payload=str(e).encode("utf-8"))

class SimpleUDPCoAPProtocol(asyncio.DatagramProtocol):
    """
    Lightweight fallback UDP listener to handle direct CoAP/UDP datagrams
    """
    def __init__(self, kafka_producer):
        self.kafka_producer = kafka_producer
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        logger.info("UDP CoAP Listener ready.")

    def datagram_received(self, data, addr):
        try:
            # Handle JSON or CoAP payload
            text = data.decode("utf-8", errors="ignore")
            # Find JSON inside UDP packet
            idx = text.find("{")
            if idx != -1:
                json_str = text[idx:]
                payload = json.loads(json_str)
                station_id = payload.get("station_id", "STN_COAP_FALLBACK")
                payload["protocol"] = "CoAP/UDP"
                payload["ingestion_timestamp"] = time.time()
                if "event_time" not in payload:
                    payload["event_time"] = time.time()

                if self.kafka_producer:
                    self.kafka_producer.send(settings.TOPIC_RAW, key=station_id, value=payload)
                    logger.debug(f"Bridged UDP/CoAP -> Kafka Station: {station_id}")
                
                # Send ack
                ack = b"\x60\x00\x00\x00" + b'{"status":"ACK"}'
                self.transport.sendto(ack, addr)
        except Exception as e:
            logger.error(f"UDP packet handling error: {e}")

class CoAPGateway:
    def __init__(self):
        self.producer = None

    def init_kafka(self):
        retries = 15
        while retries > 0:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                    retries=5
                )
                logger.info(f"Connected to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}")
                return
            except Exception as e:
                logger.warning(f"Waiting for Kafka ({settings.KAFKA_BOOTSTRAP_SERVERS})... {e}")
                time.sleep(2)
                retries -= 1

    async def start(self):
        self.init_kafka()
        
        if AIOCOAP_AVAILABLE:
            try:
                root = resource.Site()
                root.add_resource(['telemetry'], TelemetryResource(self.producer))
                root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_link_header))
                
                await aiocoap.Context.create_server_context(root, bind=(settings.COAP_HOST, settings.COAP_PORT))
                logger.info(f"CoAP aiocoap Server started on {settings.COAP_HOST}:{settings.COAP_PORT}")
                while True:
                    await asyncio.sleep(3600)
            except Exception as e:
                logger.warning(f"aiocoap server context could not bind directly ({e}), switching to UDP CoAP server...")
                loop = asyncio.get_running_loop()
                await loop.create_datagram_endpoint(
                    lambda: SimpleUDPCoAPProtocol(self.producer),
                    local_addr=(settings.COAP_HOST, settings.COAP_PORT)
                )
                logger.info(f"Fallback UDP CoAP Server listening on {settings.COAP_HOST}:{settings.COAP_PORT}")
                while True:
                    await asyncio.sleep(3600)
        else:
            loop = asyncio.get_running_loop()
            await loop.create_datagram_endpoint(
                lambda: SimpleUDPCoAPProtocol(self.producer),
                local_addr=(settings.COAP_HOST, settings.COAP_PORT)
            )
            logger.info(f"UDP CoAP Server listening on {settings.COAP_HOST}:{settings.COAP_PORT}")
            while True:
                await asyncio.sleep(3600)

if __name__ == "__main__":
    gw = CoAPGateway()
    asyncio.run(gw.start())
