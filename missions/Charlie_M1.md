**_Alice 2 (Charlie)_**
## Mission 1 : Establishing Classical Communication
*70 minutes of gameplay [70/200 points]*

As a security company which mainly focuses on spying on the technologies of other companies, you obtain an intel from your informant that Alice and Bob is developing a new communication channel based on old TV remotes.

The company Alice and Bob have quite a reputation, and you want to figure out whether their technologies are reliable (or even secure). Thanks to his expertise, your informant manages to copy over the necessary tecnical documents. **The aim of this mission is to understand what Alice and Bob are up to (by developing the same IR communication channel), and then try to see whether there is a way to spy onto their channel.**

This mission is divided into smaller tasks, which consists of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are sort of optional. It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. It is also highly advisable to split the tasks among your teammates.

#### [10 points] BREAK the ice, STOMP the ground, LIFT the air
> *This is sort of compulsory, but only to get the group going :P*

Objectives:
1. Choose a team captain,
1. Write down a short company manifesto, and
1. Take a team photo.

Point allocation scheme:
* [Full] points upon completion of the objectives.

Step by step walkthrough:
1. A good team is a team whose members knows each other pretty well.
1. A good team is also a team which can split the tasks in an efficient manner. Actually, when Mission 2 arrives, your team will be split into 2 subteam, one trying to complete Mission 1, and another one focused on hacking. So, plan well ahead.

#### [30 points] [Checkpoint] Without the electronics, there is NONE
> *Resistor: I'm gonna ask you this one time, where is the circuit?*

> *Transistor: Yeah, I'll do you one better, WHO is the circuit?*

> *Diode: I'll do YOU one better, WHY is the circuit?*

> *- 1 divided by 0*

Objective: Construct two circuits, one capable of sending IR signals, and one capable of receiving IR signals. This means, you need to emulate both Alice and Bob. The objective is accomplished when both sender and receiver circuits are built and working properly.

Upon the completion of this task, you **will receive** another copy of sender and receiver ciruit. Why? Because we are nice `GameMasters` and don't want you to repeat the same boring task :)

**Very important notes**: Read the safety precautions in Section 1.2.1 of the technical documents. This is *extremely important*, as you will get tested about this at the end of the session (no joking, confirm plus chop!).

Point allocation scheme:
* [Full] points upon correct, efficient, and stable implementation of the circuits, or
* [80%] of total points upon successful implementation of the circuits, but not necessarily correct, efficient, nor stable.

Step by step walkthrough:
1. Gather all the necessary components, and note down the polarity and the pin assignments. The facilitator will give a short lecture and demonstration about breadboard, but in case you miss it, you can refer to Section 1.2.3.
1. Construct the circuit according to the diagram, noting the polarity and the pin assignment. *If the polarity or pin assignment is incorrect, you might burn the components.* If you are unsure about certain stuffs, ask the facilitator.
1. There are two ways to proceed. <br>
[First way: the open way] Construct the sender and receiver circuit in the same breadboard using the same Arduino. However, you will need the help from the `GameMaster` to send/receive IR signals from the main computer. You might disrupt Alice and Bob in the process, as they will be doing similar stuffs at that time. This might or might not blow up your cover... <br>
[Second way: the discreet way] Construct the sender and receiver facing each other, each connected to different Arduinos, and preferably two different computers. You can send with one Arduino and receive with another one. However, you might want to cover up the devices with a box or something similar, because you don't want Alice or Bob to detect the your IR signal. Though they might ask you what the box is for...
1. Upload the Arduino program `ArduinoClassical.ino` to the correct device. You might want to use terminal command `dmesg` to look for the device address, typically in the form of `/dev/ttyACM0` or `/dev/ttyUSB0`.
1. After finish uploading, you can open the serial monitor with `Shift+Ctrl+M`. Try to send `HELP` to the Arduino, and look at the reply. Try to send blinking signal with `SBLINK`  or receive blinking signal with `RBLINK`. For sender, you should be able to see the blinking IR light with your phone camera (except iPhone). For receiver, you should see the indicator light blinking, and the serial monitor prints `BLINK!`.


#### [10 points] Asymmetrical cryptography handout
> *When cryptography is outlawed, bayl bhgynjf jvyy unir cevinpl.*

> *-  John Perry Barlow*

Objective: Complete the "asymmetrical cryptography handout". No cheating or copying with Eve allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.

Note: Only do this when there is a free time or there is a member in your group who happens to be free.


#### [20 points] [Final Task] Let make them chat
> *The Internet: transforming society and shaping the future through chat.*

> *- Dave Barry*

Objectives:
1. Successfully communicate a message from sender to receiver via the IR link by using the program `send_message.py` and `recv_message.py`,
1. Chatting (i.e. send a few messages back and forth) by using the program `chatting.py`.

Point allocation scheme:
* [Full] points by completing all the objectives **within 60 minutes** from the start of Mission 1 (leaving 10 more minutes to wrap up other tasks), or if fails,
* [80%] of total points by completing all the objectives within the time limit, or if fails,
* Maximum of [80%] of total points, proportional to the effort and the number of completed tasks at the end of the time limit.
<br><br><br>

Step by step walkthrough:
1. With the new copy of the circuit, emulate the role of Alice and Bob who tries to chat. Construct it such that the receivers and senders (for both sides) are facing each other, and that each sides are connected to different Arduino, and also preferably different computers. You might or might not need the cover box, depending on the choice that you made previously.  
1. First, test the fidelity of the signal. The sender can run `send_testQ.py` and the receiver can run `recv_testQ.py`. The programs will just send and receive `Qc!8` repeatedly. Test also for the other direction of communication. Note that you might need to modify the device address at `devloc.txt`.
1. To try sending a longer messages, the sender can run `send_message.py` and the receiver can run `recv_message.py`.
1. If everything works nicely, both sides can run `chatting.py`. One side can turn into listening mode by pressing an `Enter` button. By now you should be able to chat across computers, like what Alice and Bob is doing right now.
