''' 
------------------ RELEASE NOTE -------------------

v. 5.0.0 compatible with Tactigon Gear >= 5.0.3

This software is provided as is.
It allows to connect to Tactigon Server to train new gesture recognition model.

---------------------------------------------------
'''

import multiprocessing
import json
import tactigon_gear
from os import path
from tactigon_gear.client import Data_Collection as dc, Client
from tactigon_gear.client.models import ClientConfig, UserData, DataCollectionConfig, HAL


def main():
    """
    Starting point of the main program
    :return: None
    """

    while True:
        print("T-Gear SDK Client (v: {}), select an option:".format(tactigon_gear.__version__))
        print("Enter 0 to test server connection")
        print("Enter 1 for data collection")
        print("Enter 2 to send data to server")
        print("Enter 3 to train a new model")
        print("Enter 4 to download model from server")
        print("Type anything to EXIT")

        x = input()

        if x == "0":
            print("SERVER CONNECTION TEST")

            with open(path.join(path.dirname(__file__), "config_files", "user_data.json")) as user_data_file:
                user_data = UserData.FromJSON(json.load(user_data_file))
            
            with open(path.join(path.dirname(__file__), "config_files", "client.json")) as config_file:
                client_config = ClientConfig.FromJSON(json.load(config_file))

            with open(path.join(path.dirname(__file__), "config_files", "data_collection.json")) as dc_file:
                dc_config = DataCollectionConfig.FromJSON(json.load(dc_file))
            
            
            client = Client(user_data, client_config, dc_config)
            client.test_connection()

        elif x == "1":
            print("DATA COLLECTION")

            with open(path.join(path.dirname(__file__), "config_files", "user_data.json")) as user_data_file:
                user_data = UserData.FromJSON(json.load(user_data_file))

            with open(path.join(path.dirname(__file__), "config_files", "hal.json")) as hal_file:
                hal_config = HAL.FromJSON(json.load(hal_file))

            with open(path.join(path.dirname(__file__), "config_files", "data_collection.json")) as dc_file:
                dc_config = DataCollectionConfig.FromJSON(json.load(dc_file))

            dc.collect(user_data, hal_config, dc_config)

        elif x == "2":
            print("SERVER DATA UPLOAD")
            with open(path.join(path.dirname(__file__), "config_files", "user_data.json")) as user_data_file:
                user_data = UserData.FromJSON(json.load(user_data_file))
            
            with open(path.join(path.dirname(__file__), "config_files", "client.json")) as config_file:
                client_config = ClientConfig.FromJSON(json.load(config_file))

            with open(path.join(path.dirname(__file__), "config_files", "data_collection.json")) as dc_file:
                dc_config = DataCollectionConfig.FromJSON(json.load(dc_file))

            client = Client(user_data, client_config, dc_config)
            client.send_data()
                        
        elif x == "3":
            print("SERVER MODEL PROCESSING")

            with open(path.join(path.dirname(__file__), "config_files", "user_data.json")) as user_data_file:
                user_data = UserData.FromJSON(json.load(user_data_file))
            
            with open(path.join(path.dirname(__file__), "config_files", "client.json")) as config_file:
                client_config = ClientConfig.FromJSON(json.load(config_file))

            with open(path.join(path.dirname(__file__), "config_files", "data_collection.json")) as dc_file:
                dc_config = DataCollectionConfig.FromJSON(json.load(dc_file))

            client = Client(user_data, client_config, dc_config)
            client.train_model()

        elif x == "4":
            print("SERVER MODEL DOWNLOAD")

            with open(path.join(path.dirname(__file__), "config_files", "user_data.json")) as user_data_file:
                user_data = UserData.FromJSON(json.load(user_data_file))
            with open(path.join(path.dirname(__file__), "config_files", "client.json")) as config_file:
                client_config = ClientConfig.FromJSON(json.load(config_file))

            with open(path.join(path.dirname(__file__), "config_files", "data_collection.json")) as dc_file:
                dc_config = DataCollectionConfig.FromJSON(json.load(dc_file))

            client = Client(user_data, client_config, dc_config)
            client.download_model()

        else:
            # exit from the loop
            break

    print("Process finished")

if __name__ == "__main__":
    multiprocessing.freeze_support()  # need for pyinstaller
    main()


