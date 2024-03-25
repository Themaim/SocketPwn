import argparse
import subprocess
import threading
import time
from websocket_handler import WebSocketHandler

def parse_arguments():
    parser = argparse.ArgumentParser(description='SocketPwn: A dynamic WebSocket interaction tool with SQLMap integration.')
    parser.add_argument('-u', '--url', required=True, help='WebSocket URL to connect to.')
    parser.add_argument('--sqlmap', action='store_true', help='Flag to run SQLMap on the specified URL.')
    parser.add_argument('--payload', required=True, help='Payload template or file path with the payload template.')
    return parser.parse_args()

def read_payload(payload_arg):
    # Attempt to read from file, fallback to direct input
    try:
        with open(payload_arg, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return payload_arg

def run_sqlmap_against_middleware():
    """
    Runs SQLMap against the middleware server with the required parameters.
    """
    # This should be the URL of the local middleware server where the payload will be forwarded
    sqlmap_command = ["sqlmap", "-u", "http://localhost:8081/?id=1", "--batch"]
    try:
        subprocess.run(sqlmap_command, check=True)
        print("SQLMap operation completed.")
    except subprocess.CalledProcessError as e:
        print(f"SQLMap encountered an error: {e}")
    except FileNotFoundError:
        print("SQLMap not found. Please ensure SQLMap is installed and in your PATH.")

def main():
    args = parse_arguments()
    payload_template = read_payload(args.payload)

    if args.sqlmap:
        # Initialize and start the middleware server
        ws_handler = WebSocketHandler(args.url, payload_template)
        middleware_thread = threading.Thread(target=ws_handler.run_sqlmap_middleware, daemon=True)
        middleware_thread.start()

        # Wait for the middleware server to start before running SQLMap
        print("Waiting for the middleware server to start...")
        time.sleep(2)  # Wait time to ensure the middleware server is ready

        # Run SQLMap against the middleware server
        print("Running SQLMap...")
        run_sqlmap_against_middleware()
    else:
        print("No tool specified. Use --help for more information.")

if __name__ == '__main__':
    main()
