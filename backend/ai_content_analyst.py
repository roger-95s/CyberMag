from ollama import generate


# Content for testing
content = """
Cyber Security Analyst that will analyze the following article and provide a detailed analysis of the cyber attack, including the tactics, techniques, and procedures (TTPs) used by the threat actors, the potential impact on the targeted organization, and recommendations for mitigating similar attacks in the future.



{}
Chinese Hackers Exploit ArcGIS Server as Backdoor for Over a Year
Oct 14, 2025Ravie LakshmananCyber Espionage / Network Security

Threat actors with ties to China have been attributed to a novel campaign that compromised an ArcGIS system and turned it into a backdoor for more than a year.

The activity, per ReliaQuest, is the handiwork of a Chinese state-sponsored hacking group called Flax Typhoon, which is also tracked as Ethereal Panda and RedJuliett. According to the U.S. government, it's assessed to be a publicly-traded, Beijing-based company known as Integrity Technology Group.

"The group cleverly modified a geo-mapping application's Java server object extension (SOE) into a functioning web shell," the cybersecurity company said in a report shared with The Hacker News. "By gating access with a hardcoded key for exclusive control and embedding it in system backups, they achieved deep, long-term persistence that could survive a full system recovery."
DFIR Retainer Services

Flax Typhoon is known for living up to the "stealth" in its tradecraft by extensively incorporating living-off-the-land (LotL) methods and hands-on keyboard activity, thereby turning software components into vehicles for malicious attacks, while simultaneously evading detection.

The attack demonstrates how attackers increasingly abuse trusted tools and services to bypass security measures and gain unauthorized access to victims' systems, at the same time blending in with normal server traffic.

The "unusually clever attack chain" involved the threat actors targeting a public-facing ArcGIS server by compromising a portal administrator account to deploy a malicious SOE.

"The attackers activated the malicious SOE using a standard [JavaSimpleRESTSOE] ArcGIS extension, invoking a REST operation to run commands on the internal server via the public portal—making their activity difficult to spot," ReliaQuest said. "By adding a hard-coded key, Flax Typhoon prevented other attackers, or even curious admins, from tampering with its access."

The "web shell" is said to have been used to run network discovery operations, establish persistence by uploading a renamed SoftEther VPN executable ("bridge.exe") to the "System32" folder, and then creating a service named "SysBridge" to automatically start the binary every time the server is rebooted.

The "bridge.exe" process has been found to establish outbound HTTPS connections to an attacker-controlled IP address on port 443 with the primary goal of setting up a covert VPN channel to the external server.
CIS Build Kits

"This VPN bridge allows the attackers to extend the target's local network to a remote location, making it appear as if the attacker is part of the internal network," researchers Alexa Feminella and James Xiang explained. "This allowed them to bypass network-level monitoring, acting like a backdoor that allows them to conduct additional lateral movement and exfiltration."

The threat actors are said to have specifically targeted two workstations belonging to IT personnel in order to obtain credentials and further burrow into the network. Further investigation has uncovered that the adversary had access to the administrative account and was able to reset the password.

"This attack highlights not just the creativity and sophistication of attackers but also the danger of trusted system functionality being weaponized to evade traditional detection," the researchers noted. "It's not just about spotting malicious activity; it's about recognizing how legitimate tools and processes can be manipulated and turned against you."

"""


print("==== Generating Analysis ====")
for chunk in generate("gemma3", prompt=content, stream=True):
    print(chunk["response"], end="", flush=True)
print()  # New line at the end
