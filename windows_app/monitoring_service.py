import threading
import time
import os
import platform
import subprocess
from collections import defaultdict

class MonitoringService(threading.Thread):
    def __init__(self, api_client, interval=300, average_interval=60): # average_interval in seconds (1 minute for testing)
        super().__init__()
        self.api_client = api_client
        self.interval = interval
        self.average_interval = average_interval
        self.daemon = True
        self._stop_event = threading.Event()
        self.realtime_ping_results = {}
        self.ping_history = defaultdict(list) # Stores ping results for averaging
        self.last_average_time = time.time()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            print("MONITORING: Starting monitoring cycle...")
            try:
                hosts = self.api_client.get_hosts()
                if hosts:
                    for host in hosts:
                        if self._stop_event.is_set():
                            break
                        self.ping_host(host)
                
                # Check if it's time to calculate and submit averages
                if time.time() - self.last_average_time >= self.average_interval:
                    self.calculate_and_submit_averages()
                    self.last_average_time = time.time()

            except Exception as e:
                print(f"MONITORING: Error in monitoring cycle: {e}")

            print(f"MONITORING: Cycle finished. Sleeping for {self.interval} seconds.")
            self._stop_event.wait(self.interval)

    def ping_host(self, host):
        ip = host.get("IP_HOST")
        host_id = host.get("ID_HOST")
        if not ip or not host_id:
            return

        try:
            if platform.system().lower() == "windows":
                command = f"ping -n 1 {ip}"
                print(f"MONITORING_DEBUG: Executing command: {command}")
                result = subprocess.run(command, capture_output=True, text=True, timeout=5, shell=True)
            else:
                command = ["ping", "-c 1", ip]
                print(f"MONITORING_DEBUG: Executing command: {' '.join(command)}")
                result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            output = result.stdout
            print(f"MONITORING_DEBUG: Ping command return code: {result.returncode}")
            print(f"MONITORING_DEBUG: Ping command stdout:\n{output}")
            ping_result = None

            if result.returncode == 0:
                if platform.system().lower() == "windows":
                    for line in output.splitlines():
                        if "Media =" in line:
                            try:
                                avg_str = line.split("Media =")[1].strip().replace("ms", "")
                                ping_result = float(avg_str)
                                break
                            except ValueError:
                                pass
                else:
                    for line in output.splitlines():
                        if "time=" in line and "ms" in line:
                            try:
                                time_str = line.split("time=")[1].split(" ")[0]
                                ping_result = float(time_str)
                                break
                            except ValueError:
                                pass
            
            self.realtime_ping_results[host_id] = ping_result
            # Add to history for averaging, only if it's a valid ping result
            if ping_result is not None:
                self.ping_history[host_id].append(ping_result)

            print(f"MONITORING: Ping result for {ip}: {ping_result}ms")

            # For real-time display, we might want to send individual pings to a separate endpoint
            # or have the UI poll `realtime_ping_results`. 
            # For now, we are not sending individual pings to the API for storage.
            # The API will only receive averaged results.

        except subprocess.TimeoutExpired:
            print(f"MONITORING: Ping to {ip} timed out.")
            self.realtime_ping_results[host_id] = None
            # Do not add to ping_history for averaging if timed out
        except Exception as e:
            print(f"MONITORING: Error pinging {ip}: {e}")
            self.realtime_ping_results[host_id] = None
            # Do not add to ping_history for averaging if error

    def calculate_and_submit_averages(self):
        print("MONITORING: Calculating and submitting averages...")
        for host_id, results in self.ping_history.items():
            if results:
                average_ping = sum(results) / len(results)
                print(f"MONITORING: Submitting average ping for host {host_id}: {average_ping}ms")
                # Submit the averaged result to the API
                print(f"MONITORING_DEBUG: Attempting to submit average ping for host {host_id}: {average_ping}ms")
                self.api_client.submit_monitoreo_result(host_id, {"ping_result": average_ping})
            else:
                print(f"MONITORING: No ping results for host {host_id} in this interval.")
                # If no pings were successful, submit None or a specific value to indicate inactivity
                self.api_client.submit_monitoreo_result(host_id, {"ping_result": None})
        self.ping_history.clear() # Clear history after submitting averages
