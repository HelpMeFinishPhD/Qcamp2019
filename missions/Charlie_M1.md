**_Charlie_**
## Mission 1 : Establishing Classical Communication
*70 minutes of gameplay [70/200 points]*

As a security company which mainly focuses on spying on the technolgies of other companies, you obtain an intel from your informant that Alice and Bob is developing a new communication channel based on old TV remotes.

The company Alice and Bob have quite a reputation, and you want to figure out whether their technologies are reliable (or even secure). Thanks to his expertise, your informant manages to copy over the necessary tecnical documents. The aim of this mission is to understand what Alice and Bob are up to (by developing the same technology on your own), and then try to see whether there is a way to spy onto their channel.

The mission is further divided into smaller parts, which consists of compulsory and optional parts. The compulsory parts are marked with either [Checkpoint], [Final Mission], or [Secret Mission] flags, while the unmarked missions are sort of optional. It is thus a priority to complete all the flagged missions before the optional missions, as one will not be able to revisit this missions after the deadline. The compulsory missions also form an important basis for upcomming missions. It is also advisable to divide the mission and mission between your teammates.

### [10 points] BREAK the ice, BURN the fire, STOMP the ground, LIFT the air
> *This is sort of compulsory, but only to get the group going :P*

Objectives:
1. Choose a team captain,
1. Write down a short company manifesto, and
1. Take a team photo.

Point allocation scheme:
* [Full] points upon completion of the objectives.

### [30 points] [Checkpoint] Without the electronics, there is NONE
> *Resistor: I'm gonna ask you this one time, where is the circuit?*

> *Transistor: Yeah, I'll do you one better, WHO is the circuit?*

> *Diode: I'll do YOU one better, WHY is the circuit?*

> *- 1 divided by 0*

Objective: Construct two circuits, one capable of sending IR signals, and one capable of receiving IR signals. This means, you need to emulate both Alice and Bob. The objective is accomplished when Charlie-sender (Alice) successfully sends (and Charlie-receiver (Bob) successfully receives) the blinking signal.

Hint: You will need to refer to the technical documents. **It is very important to read all the safety precautions in the documents, as there is a chance that you might burn some electrical components, or even the arduino board. Please be careful!**

Note: Charlie-sender and Charlie-receiver needs to be perfomed on two separate arduino boards, although it is okay to use either one or two computers. With one computer, you need to use two different serial ports (and keep track which one is which). Due to budgetary constraint, the gamemaster only provides one computer, so if you want to implement this using two computers, you need to bring and use your own computer.

Point allocation scheme:
* [Full] points upon correct, efficient, and stable implementation of the circuits, or
* [80%] of total points upon successful implementation of the circuits, but not necessarily correct, efficient, nor stable.

### [10 points] Asymmetrical cryptography handout
> *When cryptography is outlawed, bayl bhgynjf jvyy unir cevinpl.*

> *-  John Perry Barlow*

Objective: Complete the "asymmetrical cryptography handout". No cheating or copying with Eve allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.

### [20 points] [Final Mission] Let make them chat
> *The Internet: transforming society and shaping the future through chat.*

> *- Dave Barry*

Objectives:
1. Successfully communicate a message from Charlie-sender to Charlie-receiver via the IR link by using the program XXX111 and XXX111,
1. Chatting (i.e. send a few messages back and forth) by using the program XXX111 and XXX111.

Point allocation scheme:
* [Full] points by completing all the objectives **within 60 minutes** from the start of Mission 1 (leaving 10 more minutes to wrap up other missions), or if fails,
* [80%] of total points by completing all the objectives within the time limit, or if fails,
* Maximum of [80%] of total points, proportional to the effort and the number of completed tasks at the end of the time limit.
