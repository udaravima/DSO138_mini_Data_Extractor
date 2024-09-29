import serial
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

'''
    Made for DSO 138 mini oscilloscope. Parameters and Plot data will saved to two separate JSON files.
    return oci_paramerters and plot_data dictionary and a list respectively.
    TODO: Format plot with parameters.
'''

if len(sys.argv) != 2 and len(sys.argv) != 4:
    print("Invalid number of arguments. Use -h or --help for more information.")
    sys.exit()
# setting up the arguments
if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print(
        "Usage: python DSO138mini.py [COM port] [baudrate (default=15200)] [output file]")
    print("Example: python DSO138mini.py COM3 115200 data.txt")
    sys.exit()

if sys.platform == "linux" or sys.platform == "linux2":
    COM = "/dev/tty" + sys.argv[1]
elif sys.platform == "win32":
    COM = sys.argv[1] if sys.argv[1].startswith("COM") else "COM" + sys.argv[1]
else:
    print("Unsupported platform")
    sys.exit()

# setting up the parameters
BAUD = int(sys.argv[2]) if sys.argv[2].isnumeric() else 115200
FILENAME = sys.argv[3]


class DSO138mini:
    def __init__(self, COM, BAUD, FILENAME="DSO138"):
        self.COM = COM
        self.BAUD = BAUD
        self.FILENAME = FILENAME

    def connect(self):

        # initialize serial connection
        try:
            self.ser = serial.Serial(
                port=self.COM, baudrate=self.BAUD, timeout=1)
        except serial.SerialException:
            print(f"Faild to open {COM} . Exiting...")
            sys.exit()
        except KeyboardInterrupt:
            print("Interrupted by User, Exiting...")
            sys.exit()

        if (self.ser.is_open):
            print("Connected to " + self.COM)

    def save_data(self):
        # open files
        save_file_param = open(self.FILENAME + "_param.json", "w")
        save_file_data = open(self.FILENAME + "_data.json", "w")
        count = 0  # counter for lines DSO138 sends 1043 lines of data
        oci_para = {}  # firtst 19 lines are parameters
        # rest of the data is plot data (1023 lines) 3 columns (seq, time, voltage)
        plot_data = []
        try:
            while True:
                if (self.ser.in_waiting):
                    data = self.ser.readline().decode("utf-8").strip().split(",")
                    if (count < 19):
                        oci_para[data[0].strip()] = data[1].strip()
                        count += 1
                    else:
                        plot_data.append(
                            [int(data[0]), int(data[1]), float(data[2])])
                        count += 1

                    if (count == 1043):
                        self.ser.close()
                        json.dump(oci_para, save_file_param)
                        json.dump(plot_data, save_file_data)
                        save_file_data.close()
                        save_file_param.close()
                        break
                    print(data, flush=True)
                else:
                    print("waiting for data...", end="\r")

        except KeyboardInterrupt:
            self.ser.close()
            json.dump(oci_para, save_file_param)
            json.dump(plot_data, save_file_data)
            save_file_data.close()
            save_file_param.close()
            print("Data saved to " + self.FILENAME)
            sys.exit()
        except serial.SerialException:
            print("Serial connection lost. Exiting...")
            sys.exit()
            
        return oci_para, plot_data

    # TODO: Format plot with parameters.
    def plot_data(self, plot_data, oci_para):
        plot_data = np.array(plot_data)
        plt.plot(plot_data[:, 1], plot_data[:, 2])
        plt.xlabel('Time (ms)')
        plt.ylabel('Voltage (V)')
        plt.title("DSO138 mini")
        x_plt = 5.5
        y_plt = 5.5
        for key, value in oci_para.items():
            plt.text(x_plt, y_plt, key + ": " + value, fontsize=12,
                     verticalalignment='top', horizontalalignment='left')
            y_plt -= 0.5

        plt.grid()
        plt.show()


def main():
    dso = DSO138mini(COM, BAUD, FILENAME)
    dso.connect()
    oci_para, plot_data = dso.save_data()
    print("Data saved to " + FILENAME)
    # dso.plot_data(plot_data, oci_para)
    return oci_para, plot_data


if __name__ == "__main__":
    main()
