from fastapi import FastAPI, HTTPException
from transitions import Machine

app = FastAPI()
            
class LightBulbFSM():
    states = ['off', 'on', 'dimmed']

    def __init__(self, name):
        self.name = name

        # Initialize the state machine
        self.machine = Machine(model=self, states=LightBulbFSM.states, initial='off')

        # Add transitions
        self.machine.add_transition(trigger='turn_on', source='off', dest='on')
        self.machine.add_transition(trigger='turn_off', source='on', dest='off')
        self.machine.add_transition(trigger='dim', source='on', dest='dimmed')
        self.machine.add_transition(trigger='brighten', source='dimmed', dest='on')
    

# Initialize the state machine (LightBulbFSM)
light_bulb = LightBulbFSM("MyLightBulb")

@app.get("/")
def root():
    """Return a welcome message."""
    return {"message": "Welcome to the Light Bulb FSM API simulation!"}


# Define the API endpoints
@app.get("/state")
def get_state():
    """Get the current state of the light bulb."""
    return {"state": light_bulb.state}

@app.post("/turn_on")
def turn_on():
    """Turn the light bulb on."""
    if light_bulb.state == 'on':
        raise HTTPException(status_code=400, detail="Light is already ON")
    light_bulb.turn_on()
    return {"message": "Light is now ON", "state": light_bulb.state}

@app.post("/turn_off")
def turn_off():
    """Turn the light bulb off."""
    if light_bulb.state == 'off':
        raise HTTPException(status_code=400, detail="Light is already OFF")
    light_bulb.turn_off()
    return {"message": "Light is now OFF", "state": light_bulb.state}

@app.post("/dim")
def dim():
    """Dim the light bulb."""
    if light_bulb.state != 'on':
        raise HTTPException(status_code=400, detail="Light must be ON to dim it")
    light_bulb.dim()
    return {"message": "Light is now DIMMED", "state": light_bulb.state}

@app.post("/brighten")
def brighten():
    """Brighten the light bulb."""
    if light_bulb.state != 'dimmed':
        raise HTTPException(status_code=400, detail="Light must be DIMMED to brighten it")
    light_bulb.brighten()
    return {"message": "Light is now ON", "state": light_bulb.state}