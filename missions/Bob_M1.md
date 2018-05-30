**_Bob 1_**
## Mission 1 : Establishing Classical Communication
*90 minutes of gameplay [80/200 points]*

As a new company in innovative telecommunications, you want to set up a communication link to your sister company, Alice. The link utilises the (old-fashioned) IR signals, similar to how the TV remote control works.

You represent the big companies, while Alice represents the common crowd. In the end, the link will be used to receive sensitive information (i.e. credit card details) from Alice. **The goal of this mission is to establish the communication link between Bob and Alice.**

This mission is divided into smaller tasks, which consist of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are optional (if you are lazy). It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. You are also strongly advised to plan the distribution of tasks among your teammates.

#### [10 points] BREAK the ice, STOMP the ground, LIFT the air
> *This is sort of compulsory, but only to get the group going :P*

Objectives:
1. Choose a team captain,
1. Write down a short company manifesto, and
1. Take a team photo.

Point allocation scheme:
* [Max] points upon completion of the objectives.

Step by step walkthrough:
1. Introduce yourself to your teammates, and tell one unique thingy about yourself... something along that line... Actually this step is a bit optional because by the end of this experiment session you probably would have known each other pretty well already :)
1. When Mission 2 arrives, your team will be split into 2 subteam, each tackling slightly different problems. So, you might want to start splitting different jobs among your teammates. You might also want to go through all the tasks in this mission to get an idea of what needs to be accomplished.

#### [20 points] [Checkpoint] Without the electronics, there is NONE
> *Resistor: I'm gonna ask you this one time, where is the circuit?*

> *Transistor: Yeah, I'll do you one better, WHO is the circuit?*

> *Diode: I'll do YOU one better, WHY is the circuit?*

> *- 1 divided by 0*

Objective: Construct a circuit capable of receiving IR signals from Alice (while at the same time Alice needs to construct another circuit capable of sending the IR signals). The objective is accomplished when Bob successfully receives (and Alice successfully sends) the blinking signal.

**Very important notes**: Read the safety precautions in Section 1.2.1 of the technical documents. This is *extremely important*, as you will get tested about this at the end of the session (not joking, we'll definitely test you!).

Point allocation scheme:
* [Full] points upon correct, efficient, and stable implementation of the circuit, or
* [80%] of total points upon successful implementation of the circuit, but not necessarily correct, efficient, nor stable.

Step by step walkthrough:
1. Gather all the necessary components, and note down the polarity and the pin assignments. The facilitator will give a short lecture and demonstration about using a breadboard, but in case you missed it, you can just refer to Section 1.2.3.
1. Construct the circuit according to the diagram, noting the polarity and the pin assignment. *If the polarity or pin assignment is incorrect, you might burn the components.* If you are unsure about anything at all, feel free to ask the facilitator.
1. Upload the Arduino program `ArduinoClassical.ino` to the correct device. You might want to use terminal command `dmesg` to look for the device address, typically in the form of `/dev/ttyACM0` or `/dev/ttyUSB0`.
1. When the upload completes, you can open the serial monitor with `Shift+Ctrl+M`. Try to send `HELP` to the Arduino, and look at the reply. Try to send blinking signal with `SBLINK` (for Alice), or receive blinking signal with `RBLINK` (for Bob). For Alice, you should be able to see the blinking IR light with your phone camera (except iPhone. Haha!). For Bob, you should see the indicator light blinking, and the serial monitor prints `BLINK!`. You may also ask the `GameMaster` to help sending/receiving IR signals from the main computer.
1. Try to perform the similar experiment, but now with Alice receiving/Bob sending instead. Remember to position the sender and receiver roughly in the line of sight.

<br>

#### [10 points] Computer does not speak words
> *The answer to the ultimate question of life, the universe and everything is 42.*

> *Technically, it is 0b101010.*

This pedagogical exercise wil dwell a little bit deeper into how information is actually sent and received. Most implementations are done in binary representation, which are in strings of 1 and 0's. Then, how can we write and read numbers, words, symbols, or even emojis in this binary string?

Objective: Alice writes the message "Hello Qcamp!" in binary representation, and sends it to Bob. You will need to use the programs in **BinaryComm Package** to perform this task, and you will also need to complete the **conversion table form**. To get maximum points, both Alice and Bob must participate in this exercise.

Point allocation scheme:
* [Max] points when both Alice and Bob successfully complete the task, or
* [50%] of total points, if only Bob takes part and completes his conversion table form.

Step by step walkthrough (optional):
1. Upload the Arduino program `send_binary.ino` (for Alice) and `recv_binary.ino` (for Bob).
1. For Alice, convert each characters from ASCII to binary, and complete the conversion table form. You can use the ASCII table, but the program `conv_ascii.py` might also be  useful.
1. For Alice, send the characters (in binary representation, i.e. `01010101`) through the serial monitor. Note that you can only send one character (one byte or 8 bits) at each time. For Bob, prepare to listen to what Alice sends via the serial monitor.
1. For Bob, after successfully receiving all the characters, convert them from binary to ASCII and complete the conversion table form.

#### [10 points] Asymmetrical cryptography handout
> *When cryptography is outlawed, bayl bhgynjf jvyy unir cevinpl.*

> *-  John Perry Barlow*

Objective: Complete the `Asymmetrical Cryptography` handout. No cheating or copying from Alice allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.

Note: Only do this when there is free time or when there is a member in your group who happens to be free.
<br>

#### [20 points] [Final Task] Let's chat with Alice
> *The Internet: transforming society and shaping the future through chat.*

> *- Dave Barry*

Objectives:
1. Successfully receive a message from Alice via the IR link by using the program `recv_message.py`,
1. Help Alice to construct the IR receiver circuit, and
1. Chat with Alice (i.e. send a few messages back and forth) by using the program `chatting.py`.

Point allocation scheme:
* [Max] points by completing all the objectives **within 75 minutes** from the start of Mission 1 (leaving 15 more minutes to wrap up other tasks), or if fails,
* [80%] of total points by completing all the objectives within the time limit, or if fails,
* Maximum of [80%] of total points, proportional to the effort and the number of completed tasks at the end of the time limit.

Step by step walkthrough:
1. First, test the fidelity of the signal. Alice can run `send_testQ.py` and Bob can run `recv_testQ.py`. The programs will just send and receive `Qc!8` repeatedly. Note that you may need to modify the device address at `devloc_classical.txt`.
1. To try sending a longer messages, Alice can run `send_message.py` and Bob can run `recv_message.py`.
1. To construct a two way communication, Alice needs to build a receiver circuit and Bob needs to build a sender circuit. Alice's member (who is now a professional) can help Bob's member in building the sender circuit, and vice versa.
1. After building them, repeat the above procedures: send and receving blinking signal, test for signal fidelity, and test to send a message (but now in the other direction).
1. If everything works nicely, both Alice and Bob can run `chatting.py`. Bob can turns into listening mode by pressing an `Enter` button. The chatting should happens both ways.

<br> <br> <br> <br> <br> <br> <br> <br>

#### *Performed __after__ the conclusion of Mission 1:*
#### [10 points] [Secret Task] Super secret messages
> *After Mission 1, a secretive agent approaches your company, as her colleague promised to send some super secret messages with the IR link that has been constructed by you and Alice. She is not certain that the IR channel is secure, but her colleague thinks so.*

There will be a few secret messages that you need to receive from Alice within 10 minutes after the conclusion of Mission 1. You need to write this secret messages on the document given by the `GameMaster`. You have to **ensure the security of the content**, and that you **seal** the document and **return** it to the `GameMaster` after the conclusion of the mission. Listen to the explicit instructions from the `GameMaster` on when to receive each messages.

Objective: Bob successfully receives all the messages from Alice.

Note: You must not communicate with Alice (no talking or signalling), except by using the chatting software developed in Mission 1.

Point allocation scheme:
* [Max] points if all the messages is sent by Alice and received successfully by Bob, or
* A fraction of [max] points, proportional to the number of messages sent and received successfully.
* Some points will be forfeited if Bob communicates with Alice in any way besides the chatting software..
