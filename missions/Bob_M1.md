**_Bob_**
## Mission 1 : Establishing Classical Communication
*90 minutes of gameplay [80/200 points]*

As a new company in innovative telecommunication industry, you want to set up a communication link to your sister company, Alice. The link utilises the (old-fashioned) IR signals, similar to how the TV remote control works.

You represent the big companies, while Alice represents the common crowd. In the end, the link will be used to receive sensitive information (i.e. credit card details) from Alice. Thus, the goal of this mission is to establish the communication link between Bob and Alice.

This mission is divided into smaller tasks, which consists of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are sort of optional. It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. It is also highly advisable to split the tasks among your teammates.

#### [10 points] BREAK the ice, STOMP the ground, LIFT the air
> *This is sort of compulsory, but only to get the group going :P*

Objectives:
1. Choose a team captain,
1. Write down a short company manifesto, and
1. Take a team photo.

Point allocation scheme:
* [Full] points upon completion of the objectives.

#### [20 points] [Checkpoint] Without the electronics, there is NONE
> *Resistor: I'm gonna ask you this one time, where is the circuit?*

> *Transistor: Yeah, I'll do you one better, WHO is the circuit?*

> *Diode: I'll do YOU one better, WHY is the circuit?*

> *- 1 divided by 0*

Objective: Construct a circuit capable of receiving IR signals from Alice (while at the same time Alice needs to construct another circuit capable of sending the IR signals). The objective is accomplished when Bob successfully receives (and Alice successfully sends) the blinking signal.

Hint: You will need to refer to the technical documents. **It is very important to read all the safety precautions in the documents, as there is a chance that you might burn some electrical components, or even the arduino board. Please be careful!**

Point allocation scheme:
* [Full] points upon correct, efficient, and stable implementation of the circuit, or
* [80%] of total points upon successful implementation of the circuit, but not necessarily correct, efficient, nor stable.

#### [10 points] Computer does not speak words
> *The answer to the ultimate question of life, the universe and everything is 42.*

> *Technically, it is 0b101010.*

This pedagogical exercise wil dwell a little bit deeper into how information is actually sent and received. Most implementations deals with binaries, which is a string of 1 and 0's. Then, how can we write and read numbers, words, symbols, or even emojis in this binary string?

Objective: Alice writes the message "Hello Qcamp!" in binary representation, and sent it to Bob. You will need to use the programs in **BinaryComm Package** to perform this task, and you will also need to complete the **conversion table form**. To get full points, both Alice and Bob must participate in this exercise.

Point allocation scheme:
* [Full] points when both Alice and Bob successfully completed the task, or
* [50%] of total points, if only Bob takes part and completes his conversion table form.

#### [10 points] Asymmetrical cryptography handout
> *When cryptography is outlawed, bayl bhgynjf jvyy unir cevinpl.*

> *-  John Perry Barlow*

Objective: Complete the "asymmetrical cryptography handout". No cheating or copying with Alice allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.

#### [20 points] [Final Task] Let's chat with Alice
> *The Internet: transforming society and shaping the future through chat.*

> *- Dave Barry*

Objectives:
1. Successfully receive a message from Alice via the IR link by using the program chatting.py,
1. Help Alice to construct the IR receiver circuit, and
1. Chat with Alice (i.e. send a few messages back and forth) by using the program chatting.py.

Point allocation scheme:
* [Full] points by completing all the objectives **within 75 minutes** from the start of Mission 1 (leaving 15 more minutes to wrap up other tasks), or if fails,
* [80%] of total points by completing all the objectives within the time limit, or if fails,
* Maximum of [80%] of total points, proportional to the effort and the number of completed tasks at the end of the time limit.

#### *Performed __after__ the conclusion of Mission 1:*
#### [10 points] [Secret Task] A super secret message
> *After Mission 1, a secretive agent approaches your company, as her colleague promised to send some super secret messages with the IR link that has been constructed by you and Alice. She is not certain that the IR channel is secure, but her colleague thinks so.*

There will be a few messages that you need to receive from Alice within 10 minutes after the conclusion of Mission 1. You need to write this secret messages down and put it inside the secret envelope to the game master. You have to ensure the security of the content, and that it does not leak out to any adversaries.

Objective: Bob successfully receives all the messages from Alice.

Note: You must not communicate with Alice (no talking or signalling), except by using the chatting software developed in Mission 1.

Point allocation scheme:
* [Full] points if all the messages is sent by Alice and received successfully by Bob, or
* A fraction of [full] points, proportional to the number of messages sent and received successfully.
* Some points will be forfeited if Bob communicate with Alice in any way besides the chatting software..
