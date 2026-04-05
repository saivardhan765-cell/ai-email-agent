from tasks import tasks
from grader import grade_all

class EmailEnv:
    def __init__(self):
        self.tasks = tasks
        self.index = 0
        self.priority=""
        self.reply=""

    def reset(self):
        self.index = 0
        return self.tasks[self.index]["email"]
    
    def step(self, action):
        task = self.tasks[self.index]
        pred = {
            "category": action,
            "priority": self.priority,
            "reply": self.reply
        }
        reward = grade_all(pred, task)
        self.index += 1
        done = self.index >= len(self.tasks)
        obs=None if done else self.tasks[self.index]["email"]
        return obs, reward, done, {}



    
    