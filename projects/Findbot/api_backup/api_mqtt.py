from fastapi import FastAPI, HTTPException
import json
import manage_db
from paho.mqtt import client as mqtt_client
import asyncio
from contextlib import asynccontextmanager
import logging      # ghi lại trạng thái kết nối và lỗi
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await start_mqtt()
    yield
    # Shutdown event (optional cleanup)
    global mqtt_client_instance
    if mqtt_client_instance and mqtt_client_instance.is_connected():
        mqtt_client_instance.loop_stop()
        mqtt_client_instance.disconnect()

app = FastAPI(title="Findbot Management API")
broker = "83073cd9910348b896c20bc695e46596.s1.eu.hivemq.cloud"  # HiveMQ public broker
port = 8883  # WebSocket port for HiveMQ public broker
topic = "Findbot/#"  # Subscribe to all Findbot-related topics
client_id = f'python-mqtt-{id(app)}'

# Global MQTT client
mqtt_client_instance = None

# Initialize database
manage_db.init_database()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Broker!")
        logger.info("Connected to HiveMQ Broker!")
        client.subscribe(topic)
    else:
        print(f"Failed to connect to HiveMQ Broker with code: {rc}")
        logger.error(f"Failed to connect to HiveMQ Broker with code: {rc}")

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    try:
        payload = json.loads(msg.payload.decode())
        if msg.topic == "Findbot/request":
            handle_mqtt_request(payload)
    except json.JSONDecodeError:
        print("Invalid JSON payload")

def handle_mqtt_request(payload):
    action = payload.get("action")
    if action == "find_product":
        result = manage_db.find_product(payload.get("product_name"))
        publish_mqtt("Findbot/response", result)
    elif action == "update_product_location":
        result = manage_db.update_product_location(
            payload.get("product_name"),
            payload.get("new_shelf_id"),
            payload.get("new_x"),
            payload.get("new_y")
        )
        publish_mqtt("Findbot/response", result)
    elif action == "update_product_name":
        result = manage_db.update_product_name(
            payload.get("product_name"),
            payload.get("new_name"),
            payload.get("location")
        )
        publish_mqtt("Findbot/response", result)
    elif action == "add_findbot":
        result = manage_db.add_findbot(
            payload.get("findbot_name"),
            payload.get("location_id")
        )
        publish_mqtt("Findbot/response", result)
    elif action == "update_findbot_location":
        result = manage_db.update_findbot_location(
            payload.get("findbot_id"),
            payload.get("new_location_id")
        )
        publish_mqtt("Findbot/response", result)
    elif action == "generate_report":
        result = manage_db.generate_report()
        publish_mqtt("Findbot/report", result)
    elif action == "delete_product":
        result = manage_db.delete_product(payload.get("product_id"))
        publish_mqtt("Findbot/delete", result)
    elif action == "undo_delete":
        result = manage_db.undo_delete()
        publish_mqtt("Findbot/undo", result)

def publish_mqtt(topic, message):
    global mqtt_client_instance
    if mqtt_client_instance and mqtt_client_instance.is_connected():
        mqtt_client_instance.publish(topic, json.dumps(message))
    else:
        print("MQTT client not connected")

# Initialize MQTT client with WebSocket support
def connect_mqtt():
    def on_connect_wrapper(client, userdata, flags, rc):
        on_connect(client, userdata, flags, rc)
    def on_message_wrapper(client, userdata, msg):
        on_message(client, userdata, msg)

    # client = mqtt_client.Client(client_id, protocol=mqtt_client.MQTTv311, transport="websockets")
    client = mqtt_client.Client(client_id, protocol=mqtt_client.MQTTv311, transport="websockets", callback_api_version=mqtt_client.CALLBACK_API_VERSION)
    client.username_pw_set("hivemq.webclient.1754058627959", "Ou29J8s,<!Tw3CDdLi:q")
    client.on_connect = on_connect_wrapper
    client.on_message = on_message_wrapper
    client.connect(broker, port)
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            client.connect(broker, port)
            return client
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed to connect: {e}")
            if attempt == max_attempts - 1:
                raise
            time.sleep(2)  # Wait 2 seconds before retry
    return client

# Start MQTT client in the background
async def start_mqtt():
    global mqtt_client_instance
    try:
        mqtt_client_instance = connect_mqtt()
        mqtt_client_instance.loop_start()
        logger.info("MQTT client started successfully")
    except Exception as e:
        logger.error(f"Failed to start MQTT client: {e}")


@app.get("/find_product/{product_name}")
async def get_find_product(product_name: str):
    result = manage_db.find_product(product_name)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    publish_mqtt("Findbot/update", result)
    return result

@app.post("/update_product_location")
async def post_update_product_location(product_name: str, new_shelf_id: int, new_x: int, new_y: int):
    result = manage_db.update_product_location(product_name, new_shelf_id, new_x, new_y)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    publish_mqtt("Findbot/update", result)
    return result

@app.post("/update_product_name")
async def post_update_product_name(product_name: str, new_name: str, location: int):
    result = manage_db.update_product_name(product_name, new_name, location)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    publish_mqtt("Findbot/update", result)
    return result

@app.post("/add_findbot")
async def post_add_findbot(findbot_name: str, location_id: int):
    result = manage_db.add_findbot(findbot_name, location_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    publish_mqtt("Findbot/update", result)
    return result

@app.post("/update_findbot_location")
async def post_update_findbot_location(findbot_id: int, new_location_id: int):
    result = manage_db.update_findbot_location(findbot_id, new_location_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    publish_mqtt("Findbot/update", result)
    return result

@app.get("/generate_report")
async def get_generate_report():
    result = manage_db.generate_report()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    publish_mqtt("Findbot/report", result)
    return result

@app.post("/delete_product")
async def post_delete_product(product_id: int):
    result = manage_db.delete_product(product_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    publish_mqtt("Findbot/delete", result)
    return result

@app.post("/undo_delete")
async def post_undo_delete():
    result = manage_db.undo_delete()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    publish_mqtt("Findbot/undo", result)
    return result

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)