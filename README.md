# manim-physics (Under Active Development)
## Introduction
This is a 2D physics simulation plugin that allows you to generate complicated scenes in various branches of Physics such as rigid mechanics, electromagnetism, wave etc.

Contributors: 
- [**pdcxs**](https://github.com/pdcxs)
- [**Matheart**](https://github.com/Matheart)
- [**Iced-Tea3**](https://github.com/Iced-Tea3)
## Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Rigid Mechanics](#rigid-mechanics)
    - [Electromagnetism](#electromagnetism)
    - [Waves](#waves)
- [Contribution Guidelines](#contribution-guidelines)
# Installation
`manim-physics` is a package on pypi, and can be directly installed using pip:
```
pip install manim-physics
```

**Warnings: Please do not directly clone the github repo! The repo is still under development and it is not a stable version, download manim-physics through pypi.**

# Usage
Make sure include these two imports at the top of the .py file
```py
from manim import *
from manim_physics import *
```
## Rigid Mechanics
Most objects can be made into a rigid body (moves according to gravity and collision) or a static body (stays still within the scene).

To use this feature, the `SpaceScene` must be used, to access the specific functions of the space.

---
**NOTE**

This feature utilizes the pymunk package. Although unnecessary, it might make it easier if you knew a few things on how to use it.

[Official Documentation](http://www.pymunk.org/en/latest/pymunk.html)

[Youtube Tutorial](https://youtu.be/pRk---rdrbo)

---
**Example**
```py
# use a SpaceScene to utilize all specific rigid-mechanics methods
class TestScene(SpaceScene):
    def construct(self):
        circle = Circle().set_fill(RED, 1).shift(RIGHT)
        ground = Line(LEFT*4,RIGHT*4,color=GREEN).shift(DOWN*3.5)
        self.add(circle,ground)

        self.make_rigid_body(circle) # Mobjects will move with gravity
        self.make_static_body(ground) # Mobjects will stay in place
        self.wait(10)
        # during wait time, the circle would move according to the simulate updater
```
![TwoObjectsFalling](/media/TwoObjectsFalling_ManimCE_v0.8.0.gif)
## Electromagnetism
This section introduces new mobjects:
- Charge
- ElectricField
- Current
- CurrentMagneticField
- BarMagnet
- BarmagneticField
```py
class ElectricFieldExampleScene(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT + DOWN)
        charge2 = Charge(2, RIGHT + DOWN)
        charge3 = Charge(-1, UP)
        field = ElectricField(charge1, charge2, charge3)
        self.add(charge1, charge2, charge3)
        self.add(field)
```
![ElectricFieldExampleScene](/media/ElectricFieldExampleScene_ManimCE_v0.8.0.png)
```py
class MagnetismExample(Scene):
    def construct(self):
        current1 = Current(LEFT * 2.5)
        current2 = Current(RIGHT * 2.5, direction=IN)
        field = CurrentMagneticField(current1, current2)
        self.add(field, current1, current2)
```
![MagnetismExample](/media/MagnetismExample_ManimCE_v0.8.0.png)
```py
class BarMagnetExample(Scene):
    def construct(self):
        bar1 = BarMagnet().rotate(PI / 2).shift(LEFT * 3.5)
        bar2 = BarMagnet().rotate(PI / 2).shift(RIGHT * 3.5)
        self.add(BarMagneticField(bar1, bar2))
        self.add(bar1, bar2)
```
![BarMagnetExample](/media/BarMagnetExample_ManimCE_v0.8.0.png)
## Waves
This section introduces new wave mobjects into manim:
- LinearWave (3D) 
- RadialWave (3D) 
- StandingWave (2D) 

```py
class LinearWaveExampleScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
        wave = LinearWave()
        self.add(wave)
        wave.start_wave()
        self.wait()
        wave.stop_wave()
```
![LinearWaveExampleScene](/media/LinearWaveExampleScene_ManimCE_v0.7.0.gif)
```py
class RadialWaveExampleScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
        wave = RadialWave(
            LEFT * 2 + DOWN * 5, # Two source of waves
            RIGHT * 2 + DOWN * 5,
            checkerboard_colors=[BLUE_D],
            stroke_width=0,
        )
        self.add(wave)
        wave.start_wave()
        self.wait()
        wave.stop_wave()
```
![RadialWaveExampleScene](/media/RadialWaveExampleScene_ManimCE_v0.7.0.gif)
```py
class StandingWaveExample(Scene):
    def construct(self):
        wave1 = StandingWave(1)
        wave2 = StandingWave(2)
        wave3 = StandingWave(3)
        wave4 = StandingWave(4)
        waves = VGroup(wave1, wave2, wave3, wave4)
        waves.arrange(DOWN).move_to(ORIGIN)
        self.add(waves)
        for wave in waves:
            wave.start_wave()
        self.wait()
```
![StandingWaveExample](/media/StandingWaveExample_ManimCE_v0.7.0.gif)
# Contribution Guidelines
The manim-physics plugin contains objects that are classified into **several main branches**, now including rigid mechanics simulation, electromagnetism and wave. 

If you want to add more objects to the plugin, The classes of the objects should be placed in the python file of corresponding branch, for example, `wave.py`, and place it under the folder src\manim_physics. The tests of objects should be named as `test_thefilename.py` such as `test_wave.py`, with some documentation, so the maintainer of this repo could ensure that it runs as expected.

## A simple Example 

```py
# use a SpaceScene to utilize all specific rigid-mechanics methods
class TestScene(SpaceScene):
    def construct(self):
        circle = Circle().set_fill(RED, 1).shift(RIGHT)
        ground = Line(LEFT*4,RIGHT*4,color=GREEN).shift(DOWN*3.5)
        self.add(circle,ground)

        self.make_rigid_body(circle) # Mobjects will move with gravity
        self.make_static_body(ground) # Mobjects will stay in place
        self.wait(10)
        # during wait time, the circle would move according to the simulate updater
```

## Other beautiful animations based on manim-physics


https://user-images.githubusercontent.com/47732475/124342625-baa96200-dbf7-11eb-996a-1f27b3625602.mp4

https://user-images.githubusercontent.com/47732475/124344045-c0587500-dc02-11eb-8fd6-afc1e5c658bb.mp4



https://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4

## Changelog
### **v0.2.1 2021.07.03**
#### New objects
- **Electromagnetism**: Charge, ElectricField, Current, CurrentMagneticField, BarMagnet, and BarMagnetField
- **Wave**: LinearWave, RadialWave, StandingWave

#### Bugfixes
- Fix typo

#### Improvements
- Simplify rigid-mechanics

### **v0.2.0 2021.07.01**
#### Breaking Changes
Objects in the manim-physics plugin are classified into several **main branches** including rigid mechanics simulation, electromagnetism and wave.