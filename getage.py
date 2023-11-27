import time
from naoqi import ALProxy

class getAge(object):
    def __init__(self):
        super(getAge, self).__init__()

    def onLoad(self):
        IP = "pepper2.local"  # Replace here with your NaoQi's IP address.
        PORT = 9559
        try:
            self.faceC = ALProxy("ALFaceCharacteristics",IP, PORT)
            self.memoryProxy = ALProxy("ALMemory", IP, PORT)
        except Exception as e:
            pass
        #    raise RuntimeError(str(e) + "Make sure you're not connected to a virtual robot." )
        self.confidence = 0.35
        self.age = 0
        self.counter = 0
        self.bIsRunning = False
        self.delayed = []
        self.errorMes = ""

    def onUnload(self):
        self.counter = 0
        self.age = 0
        self.bIsRunning = False
        self.cancelDelays()

    def onInput_onStart(self):
        try:
            #start timer
            import qi
            import functools
            delay_future = qi.async(self.onTimeout, delay=int(25 * 1000 * 1000))
            self.delayed.append(delay_future)
            bound_clean = functools.partial(self.cleanDelay, delay_future)
            delay_future.addCallback(bound_clean)
            
            self.bIsRunning = True
            while self.bIsRunning:
                if self.counter < 4:
                    try:
                        #identify user
                        ids = self.memoryProxy.getData("PeoplePerception/PeopleList")
                        
                        print("id",ids)
                        # if len(ids) == 0:
                        #     self.errorMes = "No face detected"
                        #     self.onUnload()
                        # elif len(ids) > 1:
                        #     print(len(ids))
                        #     self.errorMes = "Multiple faces detected"
                        #     self.onUnload()
                        #else:
                            #analyze age properties
                        self.faceC.analyzeFaceCharacteristics(ids[0])
                        if (len(ids)>=1 and self.welcome==False):
                            self.memoryProxy.raiseEvent("bonjour",1)
                            self.welcome=True
                        time.sleep(0.1)
                        value = self.memoryProxy.getData("PeoplePerception/Person/"+str(ids[0])+"/AgeProperties")
                        if value[1] > self.confidence:
                            self.age += value[0]
                            print("age :",self.age)
                            self.counter += 1
                    except:
                        ids = []
                else:
                    #calculate mean value
                    
                    self.age /= 4
                    print("age :",self.age)
                    self.bIsRunning=False
                    #self.onStopped(int(self.age))
                    self.onUnload()
                    return
            # raise RuntimeError(self.errorMes)
        except Exception as e:
            pass
        #     raise RuntimeError(str(e))
        #     self.onUnload()

    def onTimeout(self):
        self.errorMes = "Timeout"
        self.onUnload()

    def cleanDelay(self, fut, fut_ref):
        self.delayed.remove(fut)

    def cancelDelays(self):
        cancel_list = list(self.delayed)
        for d in cancel_list:
            d.cancel()

    def onInput_onStop(self):
        self.onUnload()


