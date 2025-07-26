import sys
sys.dont_write_bytecode = True
import xpc
import time

data = []

def average(lst):
    return sum(lst) / len(lst) if lst else 0

def monitor():
    with xpc.XPlaneConnect() as client:
        start_time = time.time()
        while True:
            try:
                posi = client.getPOSI()
                ctrl = client.getCTRL()

                loc = posi[0:3]  
                aileron = ctrl[1]  
                elevator = ctrl[0]  
                rudder = ctrl[2]  
                data.append({
                    "position": loc,
                    "aileron": aileron,
                    "elevator": elevator,
                    "rudder": rudder,
                })
                print(f"Collected Data Round {len(data)}: {data[-1]}")
                client.sendTEXT(f"Data collected successfully. Round {len(data)}")
                time.sleep(5)

                if time.time() - start_time >= 60:
                    if data:
                        avg_position = [average([d["position"][i] for d in data]) for i in range(3)]
                        avg_aileron = average([d["aileron"] for d in data])
                        avg_elevator = average([d["elevator"] for d in data])
                        avg_rudder = average([d["rudder"] for d in data])
                        print("\n1 Minute Averages") # debugging purposes and allat
                        print(f"Position: {avg_position}")
                        print(f"Aileron: {avg_aileron}")
                        print(f"Elevator: {avg_elevator}")
                        print(f"Rudder: {avg_rudder}\n")
                        client.sendTEXT(f"1 Minute Averages:\nPosition: {avg_position}\nAileron: {avg_aileron}\nElevator: {avg_elevator}\nRudder: {avg_rudder}")

                    data.clear()
                    start_time = time.time()

            except TimeoutError:
                print("No response from X-Plane.")
                time.sleep(0.5)  
            except Exception as e:
                print(f"Unexpected error: {e}")
                break  

if __name__ == "__main__":
    monitor()
