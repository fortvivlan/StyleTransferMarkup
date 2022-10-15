import os
import pandas as pd
import statistics
from time import time
from dataclasses import dataclass 
import PyQt5.QtWidgets as qtwidgets


@dataclass 
class Sentence:
    original: str 
    rewritten: str = '' 
    time: int = 0


class Handler:
    def __init__(self, result, index, path):
        self.result = result
        self.file = path
        self.index = index
        self.timecheck = False
        self.timesave = time()

    def open(self):
        filename = qtwidgets.QFileDialog.getOpenFileName()
        filepath = filename[0]
        if filepath:
            if not filepath.endswith('txt'):
                return 'not txt'
            try:
                with open(filepath, 'r', encoding='utf8') as file:
                    self.result = [Sentence(line.rstrip()) for line in file.readlines()]
                    self.file = filepath
                    return self.result[0].original
            except UnicodeDecodeError:
                return 

    def save(self):
        df = pd.DataFrame([{'original': sent.original, 'rewritten': sent.rewritten, 'time': sent.time} for sent in self.result])
        df.to_csv(f'{os.path.splitext(self.file)[0]}.csv', index=False)

    def roll(self, res, direction=True):
        if self.timecheck:
            self.result[self.index].time += time() - self.timesave
            self.timesave = time()
        if direction:
            cond = self.index >= len(self.result) - 1
        else:
            cond = self.index == 0
        if cond:
            return
        self.result[self.index].rewritten = res
        if direction:
            self.index += 1
        else:
            self.index -= 1
        return (self.result[self.index].original, self.result[self.index].rewritten)

    def statscount(self):
        timescale = [sent.time for sent in self.result if sent.rewritten]
        return [round(statistics.mean(timescale), 2), round(statistics.median(timescale), 2), round(statistics.stdev(timescale), 2), len(timescale)]