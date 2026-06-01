# Smart Cat Door Build Spec

Checked and written on April 22, 2026.

This is the more specific version of the prototype: what goes outside, what stays inside, how the flap opens, how to waterproof it, and what extra tools and parts you still need.

## Short Answer On The Parts In Your Screenshots

### 1. Duinotech / Jaycar XC4444 PIR module

- `Usable for a prototype`: yes
- `Usable fully exposed outdoors`: no
- `Best use`: mount it under a small hood so the Fresnel lens can still see out, but rain cannot sit on it
- `Important`: do not hide a PIR behind normal acrylic or glass

Links:

- Jaycar product: <https://www.jaycar.com.au/duinotech-arduino-compatible-pir-motion-detector-module/p/XC4444>
- Jaycar manual: <https://media.jaycar.com.au/product/resources/XC4444_manualMain_81363.pdf>
- Adafruit PIR explanation: <https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/how-pirs-work>

### 2. 850nm IR LED boards

- `Usable`: yes
- `Best use`: mount next to the NoIR camera under a hood or behind a clear camera window
- `Important`: the LEDs are for the camera, not for the PIR
- `Warning`: do not place them so close that the image gets washed out by reflected glare off the door or flap

### 3. Raspberry Pi Camera Module 3 NoIR

- `Best choice of the three parts you showed`: yes
- `Reason`: official Raspberry Pi camera, 12MP, autofocus, works properly in near-infrared with an IR illuminator
- `Best version`: standard FoV if the camera is a little farther back, wide FoV if the camera is mounted very close to the cat flap

Links:

- Product page: <https://www.raspberrypi.com/products/camera-module-3/>
- Camera docs: <https://www.raspberrypi.com/documentation/hardware/camera/>

## The Specific Build I Would Actually Recommend

### Outdoor side

- Camera Module 3 NoIR
- 850nm IR LED pair
- Small hood over camera + PIR
- PIR trigger sensor
- Magnetic reed switch on flap frame
- Small actuator linkage bracket on the flap

### Indoor / protected side

- Raspberry Pi Zero 2 W
- High-torque servo
- 5V power rail
- Fused power input
- Weatherproof enclosure if it still has to live near an exterior wall
- Manual override button or toggle switch

### Why this split is better

Keep the expensive electronics and motor driver side protected. Put only the sensing face and simple mechanical bits outside. That makes waterproofing much easier and failures much less annoying.

## Which Raspberry Pi To Use

### Use a Pi Zero 2 W if:

- you want Telegram alerts with a photo
- you want the PIR to act as the trigger
- you are happy to approve the cat manually from your phone

### Use a Pi 4 or Pi 5 if:

- you want automatic cat-vs-not-cat image classification on-device
- you want faster image processing
- you want more room for future features

For the first version of your build, I would still start with `Pi Zero 2 W` because it is smaller and easier to package.

## Best Trigger Strategy

For the first build, I would not rely on the PIR alone to decide “cat or not cat.”

Use this flow instead:

1. PIR detects motion near the flap.
2. Pi wakes the camera capture.
3. NoIR camera grabs a night image.
4. Telegram sends the image to your phone.
5. You choose `Open Door` or `Keep Closed`.

That is much safer than letting a PIR directly open the flap, because a PIR only tells you that something warm moved.

## Best Door Opening Method

### Recommended first version: inside-mounted servo + linkage

Use a `high-torque metal gear servo` mounted on the indoor side of the door or wall panel.

How it works:

- Servo horn rotates
- Short metal linkage or threaded rod pulls a flap bracket
- Flap opens partway
- Spring or gravity helps it close again
- Reed switch confirms that it shut properly

This is the cleanest first build because:

- it is simpler than a raw DC motor + H-bridge
- it gives you position control
- the actuator can stay dry on the indoor side

Good example servo:

- Adafruit high-torque servo: <https://www.adafruit.com/product/1142>

### If you want a stronger second version later

Use:

- 12V worm gear motor
- motor driver
- end-stop switches

That is better for a heavy flap, but it is more work than a first prototype needs.

## Waterproofing: What Actually Matters

### Camera and IR LEDs

These can sit:

- behind a clear camera window
- or under a small rain hood

For the camera, clear acrylic or polycarbonate can work as a protective front window for visible / near-IR imaging. Keep that window clean and set it slightly forward so rain does not sit directly over the lens.

### PIR sensor

This is the awkward one.

The PIR should not sit behind normal clear acrylic, polycarbonate, or glass. PIR sensors detect long-wave thermal IR, which ordinary “clear” covers do not pass well enough.

Best options:

- leave the PIR lens exposed inside a recessed hood
- or make a tiny opening just for the PIR dome
- or skip PIR completely and use camera motion detection instead

### Control box

Use:

- gasketed enclosure
- cable glands
- drip loops on every cable
- desiccant pack inside
- vent plug if condensation becomes a problem

Good enclosure and sealing parts:

- Adafruit IP65 enclosure with built-in glands: <https://www.adafruit.com/product/3931>
- Adafruit PG-7 cable gland: <https://www.adafruit.com/product/762>
- GORE outdoor enclosure vent info: <https://www.gore.com/products/protective-adhesive-vents-electronic-outdoor-enclosures>

### Fasteners and sealing

Use:

- stainless screws
- rubber washers or neoprene gasket material behind mounts
- adhesive-lined heat-shrink on solder joints
- exterior-rated silicone only around cable exits and brackets

Do not try to fully pot everything in glue. That makes maintenance miserable.

## Power Setup I Would Use

### Easiest clean setup

- `12V DC wall adapter` as the main supply
- `5V buck regulator` for the Pi and servo rail
- inline fuse near the power entry

Recommended regulator example:

- Pololu 5V 5A buck regulator: <https://www.pololu.com/product-info-merged/2851>

Why 12V in?

- easier cable runs
- easier to add stronger actuators later
- easier to keep voltage drop under control than a long 5V run

## Sensors And Parts I Would Class As “Must Have”

- Raspberry Pi Zero 2 W
- Camera Module 3 NoIR
- 850nm IR LEDs
- PIR trigger sensor or camera-only motion detection
- Magnetic reed switch
- High-torque servo
- 12V power adapter
- 5V buck regulator
- fuse holder + fuse
- weatherproof box
- cable glands
- mounting bracket / rain hood
- manual override switch

## Parts I Would Class As “Very Nice To Have”

- vent plug for condensation control
- flexible conduit for exposed wiring
- ferrules or terminal blocks for cleaner wiring
- small status LED visible from inside
- second reed switch to detect fully open state
- spring return on the flap

## Practical Tool List

You will probably want:

- drill
- step bit for cable gland holes
- small hole saw or Dremel
- screwdriver set
- wire stripper
- crimp tool
- soldering iron
- heat gun
- multimeter
- calipers or a ruler for enclosure cutouts

Optional but very helpful:

- 3D printer for the hood and brackets
- small vice
- ferrule crimper

## My Recommended Final Hardware Stack

If I had to lock the build right now, I would choose this:

- `Pi`: Raspberry Pi Zero 2 W
- `Camera`: Raspberry Pi Camera Module 3 NoIR
- `Night light`: your 850nm IR LED pair
- `Trigger`: the XC4444 PIR, mounted in a recessed hood
- `Door state`: magnetic reed switch
- `Actuator`: high-torque metal gear servo on the protected side
- `Power`: 12V adapter + 5V buck regulator + fuse
- `Enclosure`: IP65 gasketed box with cable glands

## One Important Design Decision

If you want the build to be simpler and more reliable outdoors, the smartest move is:

- outside: camera, IR LEDs, PIR lens, reed switch
- inside: Pi, power, servo, Telegram logic

That split is what I would build first.

## Source Links

- Raspberry Pi Camera Module 3: <https://www.raspberrypi.com/products/camera-module-3/>
- Raspberry Pi camera documentation: <https://www.raspberrypi.com/documentation/hardware/camera/>
- Jaycar XC4444 PIR: <https://www.jaycar.com.au/duinotech-arduino-compatible-pir-motion-detector-module/p/XC4444>
- Jaycar XC4444 manual: <https://media.jaycar.com.au/product/resources/XC4444_manualMain_81363.pdf>
- Adafruit PIR explanation: <https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/how-pirs-work>
- Adafruit high-torque servo: <https://www.adafruit.com/product/1142>
- Adafruit magnetic reed switch: <https://www.adafruit.com/product/375>
- Adafruit mini PIR: <https://www.adafruit.com/product/4871>
- Adafruit IP65 enclosure: <https://www.adafruit.com/product/3931>
- Adafruit PG-7 cable gland: <https://www.adafruit.com/product/762>
- Pololu 5V 5A buck regulator: <https://www.pololu.com/product-info-merged/2851>
- GORE protective vents: <https://www.gore.com/products/protective-adhesive-vents-electronic-outdoor-enclosures>
