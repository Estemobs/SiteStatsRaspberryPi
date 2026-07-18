import subprocess

import psutil
import requests

from config import settings


def get_temperature():
    try:
        temp = subprocess.check_output(["vcgencmd", "measure_temp"])
        return temp.decode("utf-8")
    except Exception as e:
        return str(e)


def get_ram_usage_percentage():
    ram = psutil.virtual_memory()
    return ram.percent


def get_cpu_usage_percentage():
    return psutil.cpu_percent(interval=1)


def get_ping_latency():
    try:
        ping_output = subprocess.check_output(["ping", "-c", "4", settings.ping_target])
        ping_output = ping_output.decode("utf-8")
        lines = ping_output.split("\n")
        latency_line = lines[-2]
        latency = float(latency_line.split("/")[-2])
        return latency
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    temperature = get_temperature()
    ram_usage_percentage = get_ram_usage_percentage()
    cpu_usage_percentage = get_cpu_usage_percentage()
    ping_latency = get_ping_latency()

    temp_value = temperature.split('=')[1].split("'")[0]

    response = requests.post(
        settings.api_url,
        json={
            "temperature": temp_value,
            "cpu_usage": cpu_usage_percentage,
            "ram_usage": ram_usage_percentage,
            "ping_time": ping_latency,
        },
        headers={"Authorization": f"Bearer {settings.api_token}"},
        timeout=10,
    )
    response.raise_for_status()

    print(f"Température: {temp_value}°")
    print(f"Utilisation de la RAM: {ram_usage_percentage}%")
    print(f"Utilisation du CPU: {cpu_usage_percentage}%")
    print(f"Latence (Ping): {ping_latency} ms")
