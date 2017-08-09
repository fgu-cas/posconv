#!/usr/bin/env python
import sys, os, csv, re, math

import functools
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings
from ui_posconv import Ui_PosConv


def process_file(track, has_position, cw, number):
    params = {}
    frames = []
    header = []
    for line in track:
        if re.match('^[0-9]', line):
            frames.append(line)
            continue
        elif "%Row" in line:
            line = re.sub(r"Position([^ ])", "Position \\1", line)
            line = re.sub(r"\)", "RatArenaX RatArenaY )", line)
        else:
            tmp = re.findall('%ArenaCenterXY \( ([0-9.]+) [0-9.]+ \)', line)
            if tmp:
                params["arena_x"] = float(tmp[0])
            tmp = re.findall('%ArenaCenterXY \( [0-9.]+ ([0-9.]+) \)', line)
            if tmp:
                params["arena_y"] = float(tmp[0])
        header.append(line)
    frames = [f for f in frames if f[2] is not '-1' and f[3] is not '-1']
    if has_position:
        processed_frames = calculate_arena_frame(frames, params, cw, number)
    else:
        processed_frames = simulate_arena_frame(frames, params, cw, number)
    return "".join(header + processed_frames)


def calculate_arena_frame(frames, params, cw, pulses_per_revolution):
    our_frames = []
    positions = list((float(re.split("[ ]+", x)[6]) for x in frames))

    previous_position = -1
    overflows = 0
    for i, position in enumerate(positions):
        if position > 0:
            if previous_position != -1:
                if positions[i] < previous_position:
                    overflows += 1
            previous_position = positions[i]
            positions[i] += overflows * 65535

    i = 0
    last = -1
    step = -1
    first_step = -1
    first_index = -1
    last_step = -1
    last_index = -1
    while i < len(positions):
        if positions[i] > 0:
            i2 = i + 1
            try:
                while positions[i2] < 0:
                    i2 += 1
            except IndexError:
                last_index = i
                last_step = step
                break
            step = (positions[i2] - positions[i]) / (i2 - i)
            if last == -1:
                first_index = i
                first_step = step
            last = i
        elif last != -1:
            positions[i] = positions[last] + (i - last) * step
        i += 1

    i = first_index - 1
    while i >= 0:
        positions[i] = positions[first_index] - (first_step * (first_index - i))
        i -= 1

    i = last_index + 1
    while i < len(positions):
        positions[i] = positions[last_index] + (last_step * (i - last_index))
        i += 1

    points = []
    arena_points = []
    for i, frame in enumerate(frames):
        frame_split = re.split("[ ]+", frame)
        if frame_split[2] == '-1' and frame_split[3] == '-1':
            continue
        position = positions[i] / pulses_per_revolution * 1 if cw else -1
        arena_point = rotate_point((params["arena_x"], params["arena_y"]),
                                   (float(frame_split[2]), float(frame_split[3])), position * 2 * math.pi)

        points.append((float(frame_split[2]), float(frame_split[3])))
        arena_points.append(arena_point)

        our_frames.append("%s %f %f\n" % (frame[:-1], arena_point[0], arena_point[1]))

    return our_frames


def simulate_arena_frame(frames, params, cw, revolutions_per_minute):
    our_frames = []
    for frame in frames:
        frame_split = re.split("[ ]+", frame)
        if frame_split[2] == '-1' and frame_split[3] == '-1':
            continue
        position = float(frame_split[1]) / 1000 / 60 * revolutions_per_minute * 1 if cw else -1
        arena_point = rotate_point((params["arena_x"], params["arena_y"]),
                                   (float(frame_split[2]), float(frame_split[3])), position * 2 * math.pi)
        our_frames.append("%s %f %f\n" % (frame[:-1], arena_point[0], arena_point[1]))

    return our_frames


def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


# def render_debug(center, a):
#     fig, ax = plt.subplots()
#     # ax.set_xlim([params["arena_x"]-params["diameter"]/2-5,params["arena_x"]+params["diameter"]/2+5])
#     # ax.set_ylim([params["arena_y"]-params["diameter"]/2-5,params["arena_y"]+params["diameter"]/2+5])
#     ax.set_aspect('equal', adjustable='box')
#     ax.add_artist(plt.Circle(center, 5, color='r', fill=True))
#     ax.plot([x[0] for x in a], [x[1] for x in a])
#     plt.show()


class PosConv(QDialog, Ui_PosConv):
    files = []
    settings = QSettings('FGU AV', 'PosConv')

    def __init__(self):
        QDialog.__init__(self)

        self.setupUi(self)

        self.addDirButton.clicked.connect(self.addDirButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.processButton.clicked.connect(self.processButtonClicked)
        self.simulateButton.toggled.connect(self.paramRadiosChanged)
        self.calculateButton.toggled.connect(self.paramRadiosChanged)

        self.show()

    def getDatFiles(self, directory):
        res = []
        for entry in os.listdir(directory):
            full_path = directory + "/" + entry
            if os.path.isdir(full_path):
                res += self.getDatFiles(full_path)
            elif full_path[-4:] == ".dat" and "_ARENA" not in full_path:
                res.append(full_path)
        return res

    def addDirButtonClicked(self, _):
        directory = QFileDialog.getExistingDirectory(self, "Directory with tracks", self.settings.value("lastLogs"))
        if directory:
            self.settings.setValue("lastLogs", directory)
            logs = self.getDatFiles(directory)
            logs = sorted(logs, key=os.path.getmtime)
            self.files += logs
            self.updateUI()

    def addButtonClicked(self, _):
        selected_files = \
            QFileDialog.getOpenFileNames(self, "Open tracks", self.settings.value("lastLogs"), "Logs (*.dat)")[0]
        if selected_files:
            self.settings.setValue("lastLogs", "/".join(selected_files[0].split('/')[:-1]))
            row = self.fileList.currentRow()
            if row is not -1:
                self.files[row + 1:row + 1] = selected_files
            else:
                self.files += selected_files
            self.updateUI()

    def removeButtonClicked(self, _):
        row = self.fileList.currentRow()
        if row is not -1:
            self.files.pop(row)
        self.updateUI()

    def clearButtonClicked(self, _):
        self.files.clear()
        self.updateUI()

    def paramRadiosChanged(self, _):
        if self.calculateButton.isChecked():
            self.pulsesPerRotationBox.setEnabled(True)
            self.pulsesPerRotationLabel.setEnabled(True)
            self.rpmBox.setEnabled(False)
            self.rpmLabel.setEnabled(False)
        else:
            self.pulsesPerRotationBox.setEnabled(False)
            self.pulsesPerRotationLabel.setEnabled(False)
            self.rpmBox.setEnabled(True)
            self.rpmLabel.setEnabled(True)

    def processButtonClicked(self, _):
        message = QMessageBox()
        num = 0
        cw = self.directionComboBox.currentText() == "CW"
        print(cw)
        for track in self.files:
            if self.calculateButton.isChecked():
                with open(track, 'r') as f:
                    processed = process_file(f, True, cw, self.pulsesPerRotationBox.value())
            else:
                with open(track, 'r') as f:
                    processed = process_file(f, False, cw, 1 / (self.rpmBox.value() / 60))
            filename = ".".join(track.split(".")[:-1]) + "_ARENA.dat"
            with open(filename, "w") as f:
                f.write(processed)
            num += 1
        # except:
        #   message.setText("Error, processing failed!\n%s | %s" % (sys.exc_info()[0],sys.exc_info()[1]))
        # else:
        #   message.setText("Processing successful!\nAll %n files saved with extension _ARENA." % num)
        message.exec_()

    def updateUI(self):
        self.fileList.clear()
        if len(self.files) > 0:
            self.processButton.setEnabled(True)
            for file in self.files:
                self.fileList.addItem(file)
        else:
            self.processButton.setEnabled(False)
            self.fileList.addItem("Add files...")


def main():
    app = QApplication(sys.argv)
    posconv = PosConv()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
