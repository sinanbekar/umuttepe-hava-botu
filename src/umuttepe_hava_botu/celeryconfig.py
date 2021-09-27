from .helpers import get_broker_dir, get_broker_url
import os

timezone = 'Europe/Istanbul'

broker_url = get_broker_url()
broker_dir = get_broker_dir()

broker_transport_options = {
    'data_folder_in': os.path.join(broker_dir, 'out'),
    'data_folder_out': os.path.join(broker_dir, 'out'),
    'data_folder_processed': os.path.join(broker_dir, 'processed')
}

result_persistent = False
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
worker_max_memory_per_child = 20000
