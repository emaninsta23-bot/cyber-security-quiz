from flask import Flask, render_template, jsonify, request, session
import random
import uuid

app = Flask(__name__)
app.secret_key = "cyber_quiz_2025_secret"

# Server-side session store to avoid cookie size limits
QUIZ_STORE = {}

QUESTIONS = {   'Cybercrime - Challenges & Costs': [   {   'correct': 'B',
                                               'explanation': 'Jurisdictional complexity means different legal '
                                                              'frameworks and law enforcement capabilities between '
                                                              'countries create gaps — a hacker in one country can '
                                                              'target another, making prosecution difficult.',
                                               'options': {   'A': 'Resource constraints for SMEs',
                                                              'B': 'Jurisdictional and Legal Complexities',
                                                              'C': 'Insider threats',
                                                              'D': 'Rapidly evolving threat landscape'},
                                               'question': 'Which challenge in combating cybercrime involves '
                                                           'cybercriminals operating across international borders?',
                                               'wrong_explanations': {   'A': 'Resource constraints refer to SMEs '
                                                                              'lacking budget/expertise.',
                                                                         'C': 'Insider threats are from employees or '
                                                                              'contractors with internal access.',
                                                                         'D': 'Rapidly evolving threats refer to new '
                                                                              'malware and attack techniques.'}},
                                           {   'correct': 'B',
                                               'explanation': 'AI-driven cybercrime includes automated attacks, '
                                                              'AI-generated spear-phishing emails indistinguishable '
                                                              'from legitimate ones, and more efficient/scalable '
                                                              'attacks that are harder to detect.',
                                               'options': {   'A': 'AI is only used defensively in cybersecurity — aI '
                                                                   'is used by both attackers and defenders',
                                                              'B': 'AI automates attacks, generates personalised '
                                                                   'phishing emails, and makes attacks more scalable '
                                                                   'and harder to detect',
                                                              'C': 'AI is used exclusively for password cracking — '
                                                                   'while AI can assist in password attacks, its use '
                                                                   'in cybercrime is broader',
                                                              'D': 'AI has no significant impact on cybercrime — aI '
                                                                   'has a significant and growing impact on '
                                                                   'cybercrime'},
                                               'question': 'How is AI being misused by cybercriminals according to the '
                                                           'course material?',
                                               'wrong_explanations': {   'A': 'AI is used by both attackers and '
                                                                              'defenders.',
                                                                         'C': 'While AI can assist in password '
                                                                              'attacks, its use in cybercrime is '
                                                                              'broader.',
                                                                         'D': 'AI has a significant and growing impact '
                                                                              'on cybercrime.'}},
                                           {   'correct': 'C',
                                               'explanation': 'Healthcare is particularly vulnerable — cyberattacks '
                                                              'result in theft of sensitive patient data (privacy '
                                                              'violation), legal consequences, and can disrupt '
                                                              'critical operations, delaying patient care.',
                                               'options': {   'A': 'Retail',
                                                              'B': 'Entertainment',
                                                              'C': 'Healthcare',
                                                              'D': 'Agriculture'},
                                               'question': 'Which sector is described as being particularly vulnerable '
                                                           'to cyberattacks that threaten both patient privacy and '
                                                           'critical operations?',
                                               'wrong_explanations': {   'A': 'Retail faces cyber threats (payment '
                                                                              'fraud) but critical operations '
                                                                              'disruption affecting lives is less '
                                                                              'acute.',
                                                                         'B': 'Entertainment can face piracy/data '
                                                                              'breaches but not the same life-critical '
                                                                              'risks.',
                                                                         'D': 'Agriculture is not specifically '
                                                                              'highlighted as particularly vulnerable '
                                                                              'in the course materials.'}},
                                           {   'correct': 'B',
                                               'explanation': 'The three major cost categories are: (1) Direct '
                                                              'Financial Losses (theft, fraud, ransom, recovery '
                                                              'costs), (2) Reputation Damage (loss of customer trust), '
                                                              '(3) Operational Disruption (systems offline, lost '
                                                              'productivity).',
                                               'options': {   'A': 'Hardware costs, Software costs, Training costs — '
                                                                   'hardware/software/training costs are generic IT '
                                                                   'costs, not the three categories',
                                                              'B': 'Direct financial losses, Reputation damage, '
                                                                   'Operational disruption',
                                                              'C': 'Legal fees, Investigation costs, PR costs — legal '
                                                                   'fees and PR costs fall under the broader '
                                                                   'categories, not as the primary three',
                                                              'D': 'Ransom payments, Data recovery, Staff overtime — '
                                                                   'these are specific types of direct costs, not the '
                                                                   'three categories'},
                                               'question': 'What are the three categories of costs of cybercrime?',
                                               'wrong_explanations': {   'A': 'Hardware/software/training costs are '
                                                                              'generic IT costs, not the three '
                                                                              'categories.',
                                                                         'C': 'Legal fees and PR costs fall under the '
                                                                              'broader categories, not as the primary '
                                                                              'three.',
                                                                         'D': 'These are specific types of direct '
                                                                              'costs, not the three categories.'}},
                                           {   'correct': 'C',
                                               'explanation': 'Insider threats come from employees or contractors with '
                                                              'access to sensitive information — either through '
                                                              'accidental actions or intentional malicious activity '
                                                              'like data theft or sabotage.',
                                               'options': {   'A': 'Jurisdictional complexity',
                                                              'B': 'Evolving threat landscape',
                                                              'C': 'Insider threats',
                                                              'D': 'Resource constraints'},
                                               'question': 'What type of cybercrime challenge describes when employees '
                                                           'or contractors with internal access cause security '
                                                           'breaches?',
                                               'wrong_explanations': {   'A': 'Jurisdictional complexity is about '
                                                                              'cross-border prosecution challenges.',
                                                                         'B': 'Evolving threat landscape refers to new '
                                                                              'malware and external attack techniques.',
                                                                         'D': 'Resource constraints refer to SMEs '
                                                                              'lacking cybersecurity budget and '
                                                                              'expertise.'}},
                                           {   'correct': 'B',
                                               'explanation': 'The Equifax breach is cited as an example of Reputation '
                                                              'Damage — a data breach or security failure leads to '
                                                              'long-term financial losses as customers lose trust and '
                                                              'take their business elsewhere.',
                                               'options': {   'A': 'Operational disruption — operational disruption '
                                                                   'refers to systems going offline causing lost '
                                                                   'productivity',
                                                              'B': 'Reputation damage and loss of customer trust',
                                                              'C': 'Direct financial theft — while financial losses '
                                                                   'occurred, the lecture cites it specifically as a '
                                                                   'reputation damage example',
                                                              'D': 'Regulatory fine only — regulatory fines were part '
                                                                   'of the outcome but the lecture uses it to '
                                                                   'illustrate reputation damage'},
                                               'question': 'The 2017 Equifax data breach is cited as an example of '
                                                           'which type of cybercrime cost?',
                                               'wrong_explanations': {   'A': 'Operational disruption refers to '
                                                                              'systems going offline causing lost '
                                                                              'productivity.',
                                                                         'C': 'While financial losses occurred, the '
                                                                              'lecture cites it specifically as a '
                                                                              'reputation damage example.',
                                                                         'D': 'Regulatory fines were part of the '
                                                                              'outcome but the lecture uses it to '
                                                                              'illustrate reputation damage.'}},
                                           {   'correct': 'B',
                                               'explanation': 'SMEs often lack the resources — both financial and '
                                                              'expertise — to defend against sophisticated attacks. '
                                                              'This makes them easier targets while still having '
                                                              'valuable data and systems.',
                                               'options': {   'A': 'SMEs store more data than large corporations — '
                                                                   'large corporations typically hold far more data '
                                                                   'than SMEs',
                                                              'B': 'SMEs lack the budget and expertise to defend '
                                                                   'against sophisticated cyber threats',
                                                              'C': 'SMEs are always connected to critical '
                                                                   'infrastructure — not all SMEs are connected to '
                                                                   'critical infrastructure',
                                                              'D': 'SMEs use outdated operating systems by regulation '
                                                                   '— there is no regulation requiring SMEs to use '
                                                                   'outdated systems'},
                                               'question': 'Why are Small and Medium-sized Enterprises (SMEs) '
                                                           'particularly attractive targets for cybercriminals?',
                                               'wrong_explanations': {   'A': 'Large corporations typically hold far '
                                                                              'more data than SMEs.',
                                                                         'C': 'Not all SMEs are connected to critical '
                                                                              'infrastructure.',
                                                                         'D': 'There is no regulation requiring SMEs '
                                                                              'to use outdated systems.'}},
                                           {   'correct': 'B',
                                               'explanation': "Ransomware encrypts the victim's files, making them "
                                                              'inaccessible, then demands a ransom (usually '
                                                              'cryptocurrency) for the decryption key. Examples: '
                                                              'WannaCry, REvil, LockBit.',
                                               'options': {   'A': 'Software that monitors user activity and sends it '
                                                                   'to a third party',
                                                              'B': "Malware that encrypts the victim's files and "
                                                                   'demands payment for the decryption key',
                                                              'C': 'A type of phishing attack that redirects users to '
                                                                   'fake websites',
                                                              'D': 'A network scan tool used by attackers — network '
                                                                   'scan tools are used for reconnaissance, not '
                                                                   'ransomware delivery'},
                                               'question': 'What is ransomware?',
                                               'wrong_explanations': {   'A': 'Software that monitors and exfiltrates '
                                                                              'activity is spyware.',
                                                                         'C': 'Redirecting to fake websites is '
                                                                              'pharming or phishing, not ransomware.',
                                                                         'D': 'Network scan tools are used for '
                                                                              'reconnaissance, not ransomware '
                                                                              'delivery.'}},
                                           {   'correct': 'B',
                                               'explanation': 'A zero-day vulnerability is unknown to the '
                                                              'vendor/public — there is no patch available. Attackers '
                                                              'who discover them have a significant advantage as '
                                                              'defenders have zero days to prepare a fix.',
                                               'options': {   'A': 'A vulnerability that has been known for zero days '
                                                                   "before being patched — the 'zero days' refers to "
                                                                   'zero days of warning for the vendor/defenders, not '
                                                                   'days since discovery',
                                                              'B': 'A vulnerability that is unknown to the vendor and '
                                                                   'has no available patch — attackers can exploit it '
                                                                   'with zero days for defenders to prepare',
                                                              'C': 'A vulnerability with a CVSS score of zero — a CVSS '
                                                                   'score of zero would mean no risk — not related to '
                                                                   'zero-day',
                                                              'D': 'A vulnerability that only exists on day zero of a '
                                                                   'system deployment — zero-day refers to the warning '
                                                                   'time for defenders, not deployment day'},
                                               'question': "What is a 'zero-day' vulnerability?",
                                               'wrong_explanations': {   'A': "The 'zero days' refers to zero days of "
                                                                              'warning for the vendor/defenders, not '
                                                                              'days since discovery.',
                                                                         'C': 'A CVSS score of zero would mean no risk '
                                                                              '— not related to zero-day.',
                                                                         'D': 'Zero-day refers to the warning time for '
                                                                              'defenders, not deployment day.'}},
                                           {   'correct': 'B',
                                               'explanation': 'DDoS uses a botnet — many compromised machines — to '
                                                              'simultaneously send massive traffic to a target server, '
                                                              'overwhelming its capacity and causing service '
                                                              'disruption for legitimate users.',
                                               'options': {   'A': 'An attack where a single computer floods a server '
                                                                   'with requests — a single computer attack is a DoS '
                                                                   '(Denial of Service), not Distributed',
                                                              'B': 'An attack where many compromised computers '
                                                                   '(botnet) simultaneously flood a target, '
                                                                   'overwhelming it and making it unavailable',
                                                              'C': 'An attack that intercepts and reads network '
                                                                   'traffic — intercepting network traffic is a '
                                                                   'Man-in-the-Middle attack',
                                                              'D': 'An attack that installs malware on a single target '
                                                                   'machine — installing malware on a single target is '
                                                                   'a targeted intrusion, not DDoS'},
                                               'question': 'What is a Distributed Denial of Service (DDoS) attack?',
                                               'wrong_explanations': {   'A': 'A single computer attack is a DoS '
                                                                              '(Denial of Service), not Distributed.',
                                                                         'C': 'Intercepting network traffic is a '
                                                                              'Man-in-the-Middle attack.',
                                                                         'D': 'Installing malware on a single target '
                                                                              'is a targeted intrusion, not DDoS.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Phishing uses fraudulent emails or websites '
                                                              'masquerading as legitimate entities to trick users into '
                                                              'revealing passwords, financial data, or installing '
                                                              'malware. Spear-phishing is a targeted version.',
                                               'options': {   'A': 'Scanning a network for open ports — scanning for '
                                                                   'open ports is network reconnaissance using tools '
                                                                   'like Nmap',
                                                              'B': 'A social engineering attack using deceptive emails '
                                                                   'or websites to trick users into revealing '
                                                                   'credentials or installing malware',
                                                              'C': 'Exploiting a buffer overflow vulnerability — '
                                                                   'buffer overflow exploitation is a technical '
                                                                   'vulnerability attack',
                                                              'D': 'Cracking password hashes using a dictionary attack '
                                                                   '— dictionary attacks crack passwords — phishing '
                                                                   'tricks users into handing them over'},
                                               'question': 'What is phishing?',
                                               'wrong_explanations': {   'A': 'Scanning for open ports is network '
                                                                              'reconnaissance using tools like Nmap.',
                                                                         'C': 'Buffer overflow exploitation is a '
                                                                              'technical vulnerability attack.',
                                                                         'D': 'Dictionary attacks crack passwords — '
                                                                              'phishing tricks users into handing them '
                                                                              'over.'}}],
    'Networking - IP Addresses': [   {   'correct': 'C',
                                         'explanation': 'IP stands for Internet Protocol. An IP address is a unique '
                                                        'identifier assigned to each device on a network, enabling '
                                                        'devices to communicate by specifying source and destination '
                                                        'of data packets.',
                                         'options': {   'A': 'Internal Protocol',
                                                        'B': 'Internet Pathway',
                                                        'C': 'Internet Protocol',
                                                        'D': 'Integrated Process'},
                                         'question': 'What does IP stand for?',
                                         'wrong_explanations': {   'A': 'Internal Protocol is not the correct '
                                                                        'expansion.',
                                                                   'B': 'Internet Pathway is not the correct '
                                                                        'expansion.',
                                                                   'D': 'Integrated Process is not the correct '
                                                                        'expansion.'}},
                                     {   'correct': 'B',
                                         'explanation': 'IPv4 addresses are 32-bit numbers written as four decimal '
                                                        'octets separated by periods (e.g., 192.168.1.1). Each octet '
                                                        'ranges from 0-255.',
                                         'options': {'A': '16 bits', 'B': '32 bits', 'C': '64 bits', 'D': '128 bits'},
                                         'question': 'How many bits are in an IPv4 address?',
                                         'wrong_explanations': {   'A': '16 bits is not IPv4 — that would only allow '
                                                                        '65,536 addresses.',
                                                                   'C': '64 bits is not IPv4.',
                                                                   'D': '128 bits is IPv6, not IPv4.'}},
                                     {   'correct': 'C',
                                         'explanation': 'IPv6 addresses are 128-bit numbers written as eight groups of '
                                                        'four hexadecimal digits separated by colons (e.g., '
                                                        '2001:0db8:85a3:0000:0000:8a2e:0370:7334).',
                                         'options': {'A': '32 bits', 'B': '64 bits', 'C': '128 bits', 'D': '256 bits'},
                                         'question': 'How many bits are in an IPv6 address?',
                                         'wrong_explanations': {   'A': '32 bits is IPv4.',
                                                                   'B': '64 bits is not IPv6.',
                                                                   'D': '256 bits is not a standard IP address '
                                                                        'length.'}},
                                     {   'correct': 'C',
                                         'explanation': 'Each octet in an IPv4 address ranges from 0 to 255 (8 bits = '
                                                        '2^8 = 256 possible values: 0-255).',
                                         'options': {   'A': '0 to 127',
                                                        'B': '1 to 256',
                                                        'C': '0 to 255',
                                                        'D': '0 to 254'},
                                         'question': 'What is the range of each octet in an IPv4 address?',
                                         'wrong_explanations': {   'A': '0 to 127 is only half the range (7 bits).',
                                                                   'B': '1 to 256 is incorrect — octets start at 0 and '
                                                                        'go to 255, not 256.',
                                                                   'D': '0 to 254 is sometimes used for host addresses '
                                                                        'but the full octet range is 0-255.'}},
                                     {   'correct': 'A',
                                         'explanation': 'Class A (first octet 1-126) supports up to 16,777,214 hosts '
                                                        'per network. It uses fewer bits for the network portion, '
                                                        'leaving more bits for hosts — suitable for large networks.',
                                         'options': {   'A': 'Class A (1-126)',
                                                        'B': 'Class B (128-191)',
                                                        'C': 'Class C (192-223)',
                                                        'D': 'Class D (224-239)'},
                                         'question': 'Which IPv4 address class supports the MOST hosts per network?',
                                         'wrong_explanations': {   'B': 'Class B supports up to 65,534 hosts — fewer '
                                                                        'than Class A.',
                                                                   'C': 'Class C supports only 254 hosts — used for '
                                                                        'small networks.',
                                                                   'D': 'Class D is reserved for multicasting, not '
                                                                        'regular host addressing.'}},
                                     {   'correct': 'C',
                                         'explanation': 'Class C private range is 192.168.0.0 to 192.168.255.255. '
                                                        'These are commonly used in home and office networks (e.g., '
                                                        '192.168.1.x is a typical home router subnet).',
                                         'options': {   'A': '10.0.0.0 to 10.255.255.255',
                                                        'B': '172.16.0.0 to 172.31.255.255',
                                                        'C': '192.168.0.0 to 192.168.255.255',
                                                        'D': '169.254.0.0 to 169.254.255.255'},
                                         'question': 'What is the private IP address range for Class C networks?',
                                         'wrong_explanations': {   'A': '10.0.0.0/8 is the Class A private range.',
                                                                   'B': '172.16.0.0 to 172.31.255.255 is the Class B '
                                                                        'private range.',
                                                                   'D': '169.254.0.0/16 is the APIPA (Automatic '
                                                                        'Private IP Addressing) range used when DHCP '
                                                                        'fails.'}},
                                     {   'correct': 'B',
                                         'explanation': 'Private IPs allow many devices to share a single public IP '
                                                        '(via NAT). They provide a security layer because they cannot '
                                                        'be directly accessed from the internet without NAT/port '
                                                        'forwarding.',
                                         'options': {   'A': 'They are faster than public IP addresses — private IPs '
                                                             'are not faster than public IPs',
                                                        'B': 'They allow multiple devices on a local network without '
                                                             'consuming public IPs, and cannot be accessed directly '
                                                             'from the internet',
                                                        'C': 'They are encrypted by default — private IPs are not '
                                                             'encrypted — encryption is handled by protocols like TLS',
                                                        'D': 'They are assigned by ICANN and are globally unique — '
                                                             'public IPs are assigned by ICANN/ISPs — private IPs are '
                                                             'allocated from reserved ranges'},
                                         'question': 'Why are private IP addresses important for security?',
                                         'wrong_explanations': {   'A': 'Private IPs are not faster than public IPs.',
                                                                   'C': 'Private IPs are not encrypted — encryption is '
                                                                        'handled by protocols like TLS.',
                                                                   'D': 'Public IPs are assigned by ICANN/ISPs — '
                                                                        'private IPs are allocated from reserved '
                                                                        'ranges.'}},
                                     {   'correct': 'C',
                                         'explanation': 'IPv6 was developed to solve IPv4 address exhaustion. IPv4 has '
                                                        '~4.3 billion addresses (2^32). IPv6 has 340 undecillion '
                                                        'addresses (2^128), accommodating billions of IoT and '
                                                        'connected devices.',
                                         'options': {   'A': 'IPv6 is faster than IPv4 — iPv6 can be faster in some '
                                                             'scenarios but address space was the primary driver',
                                                        'B': 'IPv6 addresses are easier to remember — iPv6 addresses '
                                                             '(hexadecimal, 128-bit) are actually harder to remember '
                                                             'than IPv4',
                                                        'C': 'To provide a much larger address space than IPv4 due to '
                                                             'the growing number of internet-connected devices',
                                                        'D': 'IPv6 includes built-in encryption — while IPv6 supports '
                                                             'IPsec natively, security was not the primary reason for '
                                                             'development'},
                                         'question': 'What is the primary reason IPv6 was developed?',
                                         'wrong_explanations': {   'A': 'IPv6 can be faster in some scenarios but '
                                                                        'address space was the primary driver.',
                                                                   'B': 'IPv6 addresses (hexadecimal, 128-bit) are '
                                                                        'actually harder to remember than IPv4.',
                                                                   'D': 'While IPv6 supports IPsec natively, security '
                                                                        'was not the primary reason for development.'}},
                                     {   'correct': 'B',
                                         'explanation': 'Subnetting divides a larger network into smaller sub-networks '
                                                        '(subnets). This improves network organisation, security '
                                                        '(isolating network segments), and efficient use of IP address '
                                                        'space.',
                                         'options': {   'A': 'Assigning public IP addresses to devices — assigning '
                                                             'public IPs is done by ISPs/DHCP, not subnetting',
                                                        'B': 'Dividing a larger network into smaller, more manageable '
                                                             'sub-networks for better organisation, security, and IP '
                                                             'efficiency',
                                                        'C': 'Converting IPv4 addresses to IPv6 — iPv4 to IPv6 '
                                                             'conversion uses transition technologies like dual-stack '
                                                             'or tunnelling',
                                                        'D': 'Blocking certain IP addresses with a firewall — blocking '
                                                             'IPs is done by firewall rules, not subnetting'},
                                         'question': 'What is subnetting?',
                                         'wrong_explanations': {   'A': 'Assigning public IPs is done by ISPs/DHCP, '
                                                                        'not subnetting.',
                                                                   'C': 'IPv4 to IPv6 conversion uses transition '
                                                                        'technologies like dual-stack or tunnelling.',
                                                                   'D': 'Blocking IPs is done by firewall rules, not '
                                                                        'subnetting.'}},
                                     {   'correct': 'B',
                                         'explanation': 'NAT allows many devices on a private network to access the '
                                                        'internet through a single public IP address. The router keeps '
                                                        'track of which internal device each connection belongs to.',
                                         'options': {   'A': 'Assigns IPv6 addresses to IPv4 devices — iPv4-to-IPv6 '
                                                             'translation uses separate transition mechanisms (not '
                                                             'standard NAT)',
                                                        'B': 'Translates private IP addresses to a public IP address, '
                                                             'allowing multiple devices to share one public IP',
                                                        'C': 'Encrypts network traffic between devices — encryption is '
                                                             'handled by TLS/IPsec, not NAT',
                                                        'D': 'Filters traffic based on firewall rules — traffic '
                                                             'filtering is done by firewalls, though many routers '
                                                             'combine NAT and firewall functions'},
                                         'question': 'What does NAT (Network Address Translation) do?',
                                         'wrong_explanations': {   'A': 'IPv4-to-IPv6 translation uses separate '
                                                                        'transition mechanisms (not standard NAT).',
                                                                   'C': 'Encryption is handled by TLS/IPsec, not NAT.',
                                                                   'D': 'Traffic filtering is done by firewalls, '
                                                                        'though many routers combine NAT and firewall '
                                                                        'functions.'}},
                                     {   'correct': 'B',
                                         'explanation': '/24 (255.255.255.0) means 24 bits identify the network and 8 '
                                                        'bits identify hosts. With 8 bits you get 256 addresses '
                                                        '(0-255), minus network (0) and broadcast (255) = 254 usable '
                                                        'host addresses.',
                                         'options': {   'A': 'A password for accessing a subnet; /24 means '
                                                             '24-character password — subnet masks have nothing to do '
                                                             'with passwords',
                                                        'B': 'A 32-bit number that defines which part of an IP address '
                                                             'is the network vs. host; /24 means the first 24 bits are '
                                                             'the network (255.255.255.0), leaving 8 bits for 254 '
                                                             'hosts',
                                                        'C': 'A type of firewall rule; /24 means port 24 is blocked — '
                                                             'firewall rules use port numbers separately — /24 is CIDR '
                                                             'notation, not a port rule',
                                                        'D': 'The number of devices allowed on a network; /24 means '
                                                             'maximum 24 devices — /24 allows 254 hosts, not 24'},
                                         'question': 'What is a subnet mask and what does /24 represent?',
                                         'wrong_explanations': {   'A': 'Subnet masks have nothing to do with '
                                                                        'passwords.',
                                                                   'C': 'Firewall rules use port numbers separately — '
                                                                        '/24 is CIDR notation, not a port rule.',
                                                                   'D': '/24 allows 254 hosts, not 24.'}},
                                     {   'correct': 'A',
                                         'explanation': 'DHCP automatically assigns network configuration (IP address, '
                                                        'subnet mask, default gateway, DNS server) to devices when '
                                                        'they join a network — eliminating the need for manual IP '
                                                        'configuration.',
                                         'options': {   'A': 'Dynamic Host Configuration Protocol — automatically '
                                                             'assigns IP addresses, subnet masks, and gateways to '
                                                             'devices on a network',
                                                        'B': 'Distributed Hash Cryptographic Protocol — encrypts IP '
                                                             'addresses — distributed Hash Cryptographic Protocol is '
                                                             'not a real term',
                                                        'C': 'Domain Host Control Panel — manages DNS entries — dNS '
                                                             'entries are managed by DNS servers, not DHCP (though '
                                                             'DHCP can provide DNS server addresses)',
                                                        'D': 'Direct HTTP Connection Protocol — routes web traffic — '
                                                             'hTTP routing is handled by web servers and proxies, not '
                                                             'DHCP'},
                                         'question': 'What is DHCP and why is it important?',
                                         'wrong_explanations': {   'B': 'Distributed Hash Cryptographic Protocol is '
                                                                        'not a real term.',
                                                                   'C': 'DNS entries are managed by DNS servers, not '
                                                                        'DHCP (though DHCP can provide DNS server '
                                                                        'addresses).',
                                                                   'D': 'HTTP routing is handled by web servers and '
                                                                        'proxies, not DHCP.'}},
                                     {   'correct': 'B',
                                         'explanation': "The Default Gateway is typically the router's IP address. "
                                                        'When a device wants to reach an IP outside its local subnet, '
                                                        'it sends the traffic to the default gateway, which routes it '
                                                        'appropriately.',
                                         'options': {   'A': 'The first device on a local network to receive DHCP '
                                                             'requests — dHCP requests can go to any DHCP server — not '
                                                             'specifically related to the default gateway',
                                                        'B': 'The router/device that forwards traffic destined for '
                                                             'outside the local subnet to the wider internet or other '
                                                             'networks',
                                                        'C': 'The DNS server that resolves domain names to IP '
                                                             'addresses — dNS resolution is done by a DNS server — a '
                                                             'separate concept from the default gateway',
                                                        'D': 'The firewall that blocks malicious traffic at the '
                                                             'network perimeter — firewalls and gateways are separate '
                                                             'devices, though some routers include firewall '
                                                             'functionality'},
                                         'question': 'What is the purpose of a Default Gateway?',
                                         'wrong_explanations': {   'A': 'DHCP requests can go to any DHCP server — not '
                                                                        'specifically related to the default gateway.',
                                                                   'C': 'DNS resolution is done by a DNS server — a '
                                                                        'separate concept from the default gateway.',
                                                                   'D': 'Firewalls and gateways are separate devices, '
                                                                        'though some routers include firewall '
                                                                        'functionality.'}}],
    'Nmap - Network Scanning': [   {   'correct': 'B',
                                       'explanation': 'Nmap = Network Mapper. Developed by Gordon Lyon (Fyodor '
                                                      'Vaskovich), it is an open-source tool for network discovery and '
                                                      'security auditing.',
                                       'options': {   'A': 'Network Management and Packet Manipulation',
                                                      'B': 'Network Mapper',
                                                      'C': 'Node Monitoring and Port Analysis',
                                                      'D': 'Network Monitoring and Penetration'},
                                       'question': 'What does Nmap stand for?',
                                       'wrong_explanations': {   'A': 'Network Management and Packet Manipulation is '
                                                                      'incorrect.',
                                                                 'C': 'Node Monitoring and Port Analysis is not what '
                                                                      'Nmap stands for.',
                                                                 'D': 'Network Monitoring and Penetration is '
                                                                      'incorrect.'}},
                                   {   'correct': 'C',
                                       'explanation': 'SYN Scan (-sS) is the default Nmap scan. It sends SYN, receives '
                                                      'SYN/ACK, but never sends ACK — completing only half the '
                                                      "handshake. This makes it stealthier as many systems don't log "
                                                      'incomplete connections.',
                                       'options': {   'A': 'TCP Connect Scan (-sT)',
                                                      'B': 'UDP Scan (-sU)',
                                                      'C': 'SYN Scan (-sS)',
                                                      'D': 'Ping Scan (-sn)'},
                                       'question': 'Which Nmap scan is stealthier because it does NOT complete the TCP '
                                                   'three-way handshake?',
                                       'wrong_explanations': {   'A': 'TCP Connect (-sT) completes the full handshake '
                                                                      '— more detectable and logged.',
                                                                 'B': 'UDP Scan discovers UDP ports — different '
                                                                      'protocol entirely.',
                                                                 'D': 'Ping Scan only checks if hosts are alive, '
                                                                      'without port scanning.'}},
                                   {   'correct': 'C',
                                       'explanation': 'CIDR notation nmap 192.168.1.0/24 scans all 256 hosts in the '
                                                      'subnet. /24 means the first 24 bits are the network portion, '
                                                      'leaving 8 bits for hosts (0-255).',
                                       'options': {   'A': 'nmap 192.168.1.1-255',
                                                      'B': 'nmap subnet 192.168.1.0',
                                                      'C': 'nmap 192.168.1.0/24',
                                                      'D': 'nmap -range 192.168.1.0'},
                                       'question': 'Which command scans all hosts in the 192.168.1.0/24 subnet?',
                                       'wrong_explanations': {   'A': 'nmap 192.168.1.1-255 also works but is less '
                                                                      'concise.',
                                                                 'B': "'subnet' is not valid Nmap syntax.",
                                                                 'D': "'-range' is not a valid Nmap flag."}},
                                   {   'correct': 'A',
                                       'explanation': 'nmap -sV probes open ports to determine the software and '
                                                      'version running (e.g., Apache 2.4.58, OpenSSH 8.0). This helps '
                                                      'identify outdated/vulnerable software.',
                                       'options': {'A': '-sV', 'B': '-O', 'C': '-p', 'D': '-A'},
                                       'question': 'Which flag enables Service Version Detection in Nmap?',
                                       'wrong_explanations': {   'B': '-O detects the operating system, not service '
                                                                      'versions.',
                                                                 'C': '-p specifies which ports to scan.',
                                                                 'D': "-A is 'aggressive scan' combining OS detection, "
                                                                      'version detection, scripts, and traceroute.'}},
                                   {   'correct': 'B',
                                       'explanation': 'NSE = Nmap Scripting Engine. It allows custom scripts for '
                                                      'vulnerability detection, exploitation checking, enumeration, '
                                                      'and more. Example: nmap --script vuln 192.168.1.1',
                                       'options': {   'A': 'Network Security Engine',
                                                      'B': 'Nmap Script Engine',
                                                      'C': 'Node Scanning Extension',
                                                      'D': 'Network Services Enumeration'},
                                       'question': 'What does NSE stand for in Nmap?',
                                       'wrong_explanations': {   'A': 'Network Security Engine is not what NSE stands '
                                                                      'for.',
                                                                 'C': 'Node Scanning Extension is incorrect.',
                                                                 'D': 'Network Services Enumeration is incorrect.'}},
                                   {   'correct': 'B',
                                       'explanation': 'nmap -O attempts to identify the operating system of the target '
                                                      'host using TCP/IP fingerprinting. This is valuable for '
                                                      'penetration testing and security assessments.',
                                       'options': {   'A': 'nmap -sV 192.168.1.1',
                                                      'B': 'nmap -O 192.168.1.1',
                                                      'C': 'nmap -sS 192.168.1.1',
                                                      'D': 'nmap -p 192.168.1.1'},
                                       'question': 'What Nmap command performs OS detection?',
                                       'wrong_explanations': {   'A': '-sV is service version detection.',
                                                                 'C': '-sS is the stealth SYN scan.',
                                                                 'D': '-p specifies port ranges.'}},
                                   {   'correct': 'B',
                                       'explanation': 'nmap -oX saves results in XML format. Other output options: -oN '
                                                      '(normal text), -oG (greppable). XML output is useful for '
                                                      'importing into other tools.',
                                       'options': {   'A': 'nmap -oN output.xml 192.168.1.1',
                                                      'B': 'nmap -oX output.xml 192.168.1.1',
                                                      'C': 'nmap -oG output.xml 192.168.1.1',
                                                      'D': 'nmap --save-xml output.xml 192.168.1.1'},
                                       'question': 'Which Nmap command saves scan results to an XML file?',
                                       'wrong_explanations': {   'A': '-oN saves in normal text format, not XML.',
                                                                 'C': '-oG saves in greppable format.',
                                                                 'D': '--save-xml is not a valid Nmap flag.'}},
                                   {   'correct': 'C',
                                       'explanation': 'nmap -D RND:10 uses 10 random decoy IP addresses alongside the '
                                                      'real scanner, making it harder to determine which IP is '
                                                      'actually performing the scan.',
                                       'options': {   'A': 'nmap -f 192.168.1.1',
                                                      'B': 'nmap -sI zombie_host 192.168.1.1',
                                                      'C': 'nmap -D RND:10 192.168.1.1',
                                                      'D': 'nmap --spoof-mac 00:11:22:33:44:55 192.168.1.1'},
                                       'question': 'Which advanced Nmap technique uses decoy IP addresses to obscure '
                                                   'the true scanner?',
                                       'wrong_explanations': {   'A': 'nmap -f uses packet fragmentation to bypass '
                                                                      'firewalls.',
                                                                 'B': 'nmap -sI performs an Idle/zombie scan using a '
                                                                      'third-party host.',
                                                                 'D': 'nmap --spoof-mac spoofs the MAC address, not IP '
                                                                      'addresses.'}},
                                   {   'correct': 'C',
                                       'explanation': 'nmap -sU performs a UDP scan to discover open UDP ports. UDP '
                                                      'services (DNS port 53, DHCP port 67/68, SNMP port 161) are '
                                                      'often overlooked but can be vulnerable.',
                                       'options': {   'A': 'nmap -sS 192.168.1.1',
                                                      'B': 'nmap -sT 192.168.1.1',
                                                      'C': 'nmap -sU 192.168.1.1',
                                                      'D': 'nmap -sn 192.168.1.1'},
                                       'question': 'Which Nmap scan type discovers open UDP ports?',
                                       'wrong_explanations': {   'A': '-sS is the TCP SYN scan.',
                                                                 'B': '-sT is the TCP Connect scan.',
                                                                 'D': '-sn is the ping scan (host discovery only, no '
                                                                      'port scan).'}},
                                   {   'correct': 'B',
                                       'explanation': 'The Idle Scan (-sI) uses a zombie host (an idle third-party '
                                                      'machine) to send packets on behalf of the scanner. The target '
                                                      "sees the zombie's IP, completely hiding the true scanner's "
                                                      'identity.',
                                       'options': {   'A': 'A scan that runs in the background without using CPU — '
                                                           'background scanning is a scheduling concept, not what Idle '
                                                           'Scan means',
                                                      'B': 'A stealthy scan that uses a third-party zombie host to '
                                                           "perform the scan — hiding the true scanner's IP",
                                                      'C': 'A slow scan to avoid detection by rate-limiting — slow '
                                                           'scanning to avoid detection uses timing options (-T0 to '
                                                           '-T5)',
                                                      'D': 'A scan that only runs when the system is idle — running '
                                                           'during system idle time is not what this scan does'},
                                       'question': "What is an 'Idle Scan' in Nmap (-sI)?",
                                       'wrong_explanations': {   'A': 'Background scanning is a scheduling concept, '
                                                                      'not what Idle Scan means.',
                                                                 'C': 'Slow scanning to avoid detection uses timing '
                                                                      'options (-T0 to -T5).',
                                                                 'D': 'Running during system idle time is not what '
                                                                      'this scan does.'}},
                                   {   'correct': 'B',
                                       'explanation': 'Nmap timing templates control scan speed: T0 (Paranoid - very '
                                                      'slow, avoids IDS), T1 (Sneaky), T2 (Polite), T3 (Normal '
                                                      'default), T4 (Aggressive), T5 (Insane - fastest but may miss '
                                                      'results).',
                                       'options': {   'A': 'How many ports are scanned — port range is controlled with '
                                                           '-p, not -T',
                                                      'B': 'The speed/aggressiveness of the scan — -T0 is slowest '
                                                           '(paranoid), -T5 is fastest (insane)',
                                                      'C': 'The number of parallel scan threads — parallelism is '
                                                           'controlled with --min-parallelism/--max-parallelism',
                                                      'D': 'The output format of the scan results — output format is '
                                                           'controlled with -oN, -oX, -oG'},
                                       'question': 'What do Nmap timing templates (-T0 to -T5) control?',
                                       'wrong_explanations': {   'A': 'Port range is controlled with -p, not -T.',
                                                                 'C': 'Parallelism is controlled with '
                                                                      '--min-parallelism/--max-parallelism.',
                                                                 'D': 'Output format is controlled with -oN, -oX, '
                                                                      '-oG.'}},
                                   {   'correct': 'B',
                                       'explanation': 'nmap -A enables Aggressive mode, combining: -O (OS detection), '
                                                      '-sV (version detection), -sC (default scripts), and '
                                                      '--traceroute. Useful for comprehensive audits but very noisy.',
                                       'options': {   'A': 'Scans all 65535 ports — scanning all ports uses -p- or -p '
                                                           '1-65535',
                                                      'B': 'Enables aggressive mode: OS detection, version detection, '
                                                           'script scanning, and traceroute combined',
                                                      'C': "Performs an anonymous scan hiding the scanner's IP — nmap "
                                                           '-A does not hide your IP — use -D for decoys',
                                                      'D': 'Scans using UDP instead of TCP — uDP scanning uses -sU'},
                                       'question': 'What does the nmap -A flag do?',
                                       'wrong_explanations': {   'A': 'Scanning all ports uses -p- or -p 1-65535.',
                                                                 'C': 'Nmap -A does not hide your IP — use -D for '
                                                                      'decoys.',
                                                                 'D': 'UDP scanning uses -sU.'}},
                                   {   'correct': 'B',
                                       'explanation': 'In a SYN Scan: Scanner sends SYN, open port responds with '
                                                      "SYN/ACK (confirming it's open), then Scanner sends RST to tear "
                                                      'down without completing the connection — stealth avoids full '
                                                      'session logging.',
                                       'options': {   'A': 'Scanner sends SYN → Target sends RST → Scanner ignores — a '
                                                           'RST response indicates the port is CLOSED, not open',
                                                      'B': 'Scanner sends SYN → Target sends SYN/ACK → Scanner sends '
                                                           'RST (not ACK), completing only half the handshake',
                                                      'C': 'Scanner sends SYN → Target sends SYN → Both send ACK — the '
                                                           'handshake sequence is wrong — SYN is always first from the '
                                                           'initiator',
                                                      'D': 'Scanner sends ACK → Target sends SYN/ACK → Scanner sends '
                                                           'SYN — the sequence starts with SYN from the scanner, not '
                                                           'ACK'},
                                       'question': 'In the Nmap TCP three-way handshake, what happens during a SYN '
                                                   'Scan when a port is open?',
                                       'wrong_explanations': {   'A': 'A RST response indicates the port is CLOSED, '
                                                                      'not open.',
                                                                 'C': 'The handshake sequence is wrong — SYN is always '
                                                                      'first from the initiator.',
                                                                 'D': 'The sequence starts with SYN from the scanner, '
                                                                      'not ACK.'}},
                                   {   'correct': 'B',
                                       'explanation': "nmap --script vuln runs NSE scripts in the 'vuln' category to "
                                                      'check for known vulnerabilities on discovered services — e.g., '
                                                      'checking for EternalBlue (MS17-010) on Windows SMB.',
                                       'options': {   'A': 'Lists all Nmap scripts available — listing scripts uses '
                                                           '--script-help all or nmap --script-help',
                                                      'B': 'Runs Nmap Scripting Engine vulnerability detection scripts '
                                                           'against the target',
                                                      'C': 'Generates a vulnerability report in PDF format — nmap does '
                                                           'not generate PDFs — use -oX then convert',
                                                      'D': 'Exports scan results to Nessus — nmap cannot directly '
                                                           'export to Nessus format'},
                                       'question': 'What is the purpose of nmap --script vuln?',
                                       'wrong_explanations': {   'A': 'Listing scripts uses --script-help all or nmap '
                                                                      '--script-help.',
                                                                 'C': 'Nmap does not generate PDFs — use -oX then '
                                                                      'convert.',
                                                                 'D': 'Nmap cannot directly export to Nessus '
                                                                      'format.'}}],
    'SSH - Secure Shell': [   {   'correct': 'B',
                                  'explanation': 'SSH (Secure Shell) is a cryptographic network protocol for secure '
                                                 'remote access over unsecured networks — used for login, command '
                                                 'execution, and data transfer.',
                                  'options': {   'A': 'Encrypting files on local drives — local file encryption uses '
                                                      'BitLocker, FileVault, etc',
                                                 'B': 'Providing secure remote login, command execution, and data '
                                                      'transfer over unsecured networks',
                                                 'C': 'Monitoring network traffic — traffic monitoring is done by '
                                                      'IDS/IPS tools',
                                                 'D': 'Managing firewall rules — firewalls have dedicated management '
                                                      'interfaces (though you can access them via SSH)'},
                                  'question': 'What is SSH primarily used for?',
                                  'wrong_explanations': {   'A': 'Local file encryption uses BitLocker, FileVault, '
                                                                 'etc.',
                                                            'C': 'Traffic monitoring is done by IDS/IPS tools.',
                                                            'D': 'Firewalls have dedicated management interfaces '
                                                                 '(though you can access them via SSH).'}},
                              {   'correct': 'C',
                                  'explanation': 'ssh-keygen generates key pairs. -t rsa = RSA type, -b 4096 = '
                                                 '4096-bit key, -C adds a comment label (usually email).',
                                  'options': {   'A': 'ssh-copy-id -t rsa -b 4096 — ssh-copy-id copies your public key '
                                                      "to a remote server — it doesn't generate keys",
                                                 'B': 'ssh -t rsa -b 4096 username@host — ssh is the connection '
                                                      'command, not for key generation',
                                                 'C': "ssh-keygen -t rsa -b 4096 -C 'email@example.com'",
                                                 'D': 'ssh-agent -t rsa -b 4096 — ssh-agent manages keys in memory but '
                                                      "doesn't generate them"},
                                  'question': 'Which SSH command generates a 4096-bit RSA key pair?',
                                  'wrong_explanations': {   'A': 'ssh-copy-id copies your public key to a remote '
                                                                 "server — it doesn't generate keys.",
                                                            'B': 'ssh is the connection command, not for key '
                                                                 'generation.',
                                                            'D': "ssh-agent manages keys in memory but doesn't "
                                                                 'generate them.'}},
                              {   'correct': 'B',
                                  'explanation': 'Password-based SSH is vulnerable to brute-force attacks. Tools like '
                                                 'fail2ban temporarily block IPs after multiple failed attempts. '
                                                 'Key-based authentication is more secure.',
                                  'options': {   'A': 'SSH does not support file transfer — sSH supports file transfer '
                                                      'via SCP and SFTP',
                                                 'B': 'Password-based SSH is vulnerable to brute-force attacks without '
                                                      'protections like fail2ban',
                                                 'C': 'SSH cannot be used on Linux — sSH is widely supported on Linux, '
                                                      'macOS, and Windows',
                                                 'D': 'SSH requires a paid enterprise licence — sSH is an open '
                                                      'standard — free to use'},
                                  'question': 'Which is a limitation of SSH?',
                                  'wrong_explanations': {   'A': 'SSH supports file transfer via SCP and SFTP.',
                                                            'C': 'SSH is widely supported on Linux, macOS, and '
                                                                 'Windows.',
                                                            'D': 'SSH is an open standard — free to use.'}},
                              {   'correct': 'B',
                                  'explanation': 'The -p flag specifies the port. Default SSH port is 22. Using a '
                                                 'non-standard port (like 2222) can reduce automated brute-force '
                                                 'attempts.',
                                  'options': {   'A': 'ssh --port 2222 alice@192.168.1.10',
                                                 'B': 'ssh -p 2222 alice@192.168.1.10',
                                                 'C': 'ssh alice@192.168.1.10:2222',
                                                 'D': 'ssh /port=2222 alice@192.168.1.10'},
                                  'question': 'What SSH command connects on a non-standard port (e.g., port 2222)?',
                                  'wrong_explanations': {   'A': 'SSH uses -p not --port.',
                                                            'C': 'host:port colon notation is not standard SSH syntax.',
                                                            'D': '/port= is not valid SSH syntax.'}},
                              {   'correct': 'B',
                                  'explanation': 'SCP (Secure Copy Protocol) uses SSH to securely transfer files '
                                                 'between a local and remote host. Example: scp file.txt '
                                                 'alice@192.168.1.10:/remote/path',
                                  'options': {   'A': 'Secure Configuration Protocol — secure Configuration Protocol '
                                                      'is not what SCP stands for in SSH',
                                                 'B': 'Secure Copy Protocol — used to securely copy files between '
                                                      'hosts over SSH',
                                                 'C': 'System Control Process — system Control Process is not what SCP '
                                                      'stands for',
                                                 'D': 'Server Certificate Provider — certificate management is done by '
                                                      'PKI systems, not SCP'},
                                  'question': 'What is SCP in the context of SSH?',
                                  'wrong_explanations': {   'A': 'Secure Configuration Protocol is not what SCP stands '
                                                                 'for in SSH.',
                                                            'C': 'System Control Process is not what SCP stands for.',
                                                            'D': 'Certificate management is done by PKI systems, not '
                                                                 'SCP.'}},
                              {   'correct': 'B',
                                  'explanation': "ssh-copy-id installs the local user's public key in the remote "
                                                 "server's ~/.ssh/authorized_keys file, enabling passwordless "
                                                 '(key-based) authentication.',
                                  'options': {   'A': 'ssh-keygen --install alice@192.168.1.10',
                                                 'B': 'ssh-copy-id alice@192.168.1.10',
                                                 'C': 'scp ~/.ssh/id_rsa alice@192.168.1.10',
                                                 'D': 'ssh --authorize alice@192.168.1.10'},
                                  'question': 'Which command copies the local public key to a remote server to enable '
                                              'passwordless login?',
                                  'wrong_explanations': {   'A': 'ssh-keygen --install is not valid syntax.',
                                                            'C': 'scp copies the PRIVATE key — never copy your private '
                                                                 'key to a remote server.',
                                                            'D': 'ssh --authorize is not valid SSH syntax.'}},
                              {   'correct': 'B',
                                  'explanation': 'SSH Port Forwarding (tunnelling) allows local ports to securely '
                                                 'connect to services on remote machines — e.g., securely accessing a '
                                                 "remote database that isn't publicly exposed.",
                                  'options': {   'A': 'Opening multiple simultaneous SSH connections — multiple '
                                                      'connections are supported by SSH multiplexing, not specifically '
                                                      'port forwarding',
                                                 'B': 'Local ports to securely connect to services on remote machines '
                                                      'through the SSH tunnel',
                                                 'C': "SSH to run on any port automatically — port forwarding doesn't "
                                                      'change the SSH daemon port automatically',
                                                 'D': 'Forwarding SSH login credentials to a proxy server — forwarding '
                                                      'credentials to a proxy is a security risk, not what port '
                                                      'forwarding does'},
                                  'question': "What does SSH's Port Forwarding allow?",
                                  'wrong_explanations': {   'A': 'Multiple connections are supported by SSH '
                                                                 'multiplexing, not specifically port forwarding.',
                                                            'C': "Port forwarding doesn't change the SSH daemon port "
                                                                 'automatically.',
                                                            'D': 'Forwarding credentials to a proxy is a security '
                                                                 'risk, not what port forwarding does.'}},
                              {   'correct': 'C',
                                  'explanation': 'In large organisations, SSH key management is complex — distributing '
                                                 'keys, rotating them, revoking access, and ensuring only authorised '
                                                 'keys are present across hundreds of systems requires dedicated tools '
                                                 'and processes.',
                                  'options': {   'A': 'SSH keys expire after 30 days automatically — sSH keys do not '
                                                      'have a built-in 30-day expiry',
                                                 'B': 'SSH only supports a maximum of 10 simultaneous connections — '
                                                      'sSH has no built-in 10-connection limit',
                                                 'C': 'Managing and distributing SSH keys becomes challenging at '
                                                      'scale, especially with many users and systems',
                                                 'D': 'SSH keys cannot be stored on hardware security modules — sSH '
                                                      'keys can be stored on HSMs — this is actually a security best '
                                                      'practice'},
                                  'question': 'What is one key limitation of SSH involving key management in large '
                                              'organisations?',
                                  'wrong_explanations': {   'A': 'SSH keys do not have a built-in 30-day expiry.',
                                                            'B': 'SSH has no built-in 10-connection limit.',
                                                            'D': 'SSH keys can be stored on HSMs — this is actually a '
                                                                 'security best practice.'}},
                              {   'correct': 'B',
                                  'explanation': 'The authorized_keys file on the server stores the public keys of '
                                                 'clients allowed to connect. When a client connects, the server '
                                                 'checks if their public key is in this file to grant passwordless '
                                                 'access.',
                                  'options': {   'A': "It stores the server's private key — the server's private key "
                                                      'is stored in /etc/ssh/ (e.g., ssh_host_rsa_key)',
                                                 'B': 'It lists the public keys of clients who are permitted to log in '
                                                      'without a password',
                                                 'C': 'It logs all SSH connection attempts — sSH connection logs are '
                                                      'in /var/log/auth.log or /var/log/secure',
                                                 'D': 'It contains the SSH server configuration — sSH server '
                                                      'configuration is in /etc/ssh/sshd_config'},
                                  'question': 'What is the purpose of the ~/.ssh/authorized_keys file on a server?',
                                  'wrong_explanations': {   'A': "The server's private key is stored in /etc/ssh/ "
                                                                 '(e.g., ssh_host_rsa_key).',
                                                            'C': 'SSH connection logs are in /var/log/auth.log or '
                                                                 '/var/log/secure.',
                                                            'D': 'SSH server configuration is in '
                                                                 '/etc/ssh/sshd_config.'}},
                              {   'correct': 'B',
                                  'explanation': 'SSH key-based auth: server sends a challenge, client signs it with '
                                                 'their private key, server verifies the signature using the stored '
                                                 'public key. The private key never leaves the client.',
                                  'options': {   'A': 'The client sends the private key to the server for verification '
                                                      '— the private key NEVER leaves the client — sending it would be '
                                                      'catastrophic',
                                                 'B': 'The client proves possession of the private key by signing a '
                                                      'challenge from the server — the server verifies using the '
                                                      'stored public key',
                                                 'C': 'Both client and server share the same symmetric key — sSH uses '
                                                      'asymmetric cryptography for authentication (key pairs), not '
                                                      'shared symmetric keys',
                                                 'D': 'The server sends a hash of the password for the client to '
                                                      'compare — password hashing comparison is not how key-based SSH '
                                                      'auth works'},
                                  'question': 'How does SSH key-based authentication work?',
                                  'wrong_explanations': {   'A': 'The private key NEVER leaves the client — sending it '
                                                                 'would be catastrophic.',
                                                            'C': 'SSH uses asymmetric cryptography for authentication '
                                                                 '(key pairs), not shared symmetric keys.',
                                                            'D': 'Password hashing comparison is not how key-based SSH '
                                                                 'auth works.'}},
                              {   'correct': 'B',
                                  'explanation': 'SFTP uses SSH to encrypt file transfers — authentication and data '
                                                 'are both protected. Standard FTP transmits credentials and file '
                                                 'contents in plaintext, making it vulnerable to eavesdropping.',
                                  'options': {   'A': 'SFTP is faster than FTP because it compresses data — speed is '
                                                      'not the key difference — encryption is',
                                                 'B': 'SFTP (SSH File Transfer Protocol) runs over an SSH tunnel and '
                                                      'encrypts data in transit; FTP transmits everything in plaintext',
                                                 'C': 'SFTP only works on Linux; FTP works on all operating systems — '
                                                      'both SFTP and FTP are cross-platform',
                                                 'D': 'SFTP and FTP are identical — just different names — they are '
                                                      'fundamentally different — SFTP is secure, FTP is not'},
                                  'question': 'What is SFTP and how does it differ from FTP?',
                                  'wrong_explanations': {   'A': 'Speed is not the key difference — encryption is.',
                                                            'C': 'Both SFTP and FTP are cross-platform.',
                                                            'D': 'They are fundamentally different — SFTP is secure, '
                                                                 'FTP is not.'}},
                              {   'correct': 'B',
                                  'explanation': 'Disabling direct root SSH login means attackers cannot brute-force '
                                                 'or exploit root directly. They must first gain access as a regular '
                                                 'user, then escalate — adding an extra step and reducing the attack '
                                                 'surface.',
                                  'options': {   'A': 'Prevents the root account from existing on the server — the '
                                                      'root account still exists locally — only SSH login is blocked',
                                                 'B': 'Forces attackers to first compromise a regular user account '
                                                      'before attempting privilege escalation, adding an extra '
                                                      'security layer',
                                                 'C': 'Disables SSH entirely for all users — only root SSH access is '
                                                      'disabled — other users can still SSH in',
                                                 'D': 'Makes root login require two-factor authentication — disabling '
                                                      "root login doesn't automatically enable 2FA"},
                                  'question': 'What does disabling SSH root login (PermitRootLogin no) achieve?',
                                  'wrong_explanations': {   'A': 'The root account still exists locally — only SSH '
                                                                 'login is blocked.',
                                                            'C': 'Only root SSH access is disabled — other users can '
                                                                 'still SSH in.',
                                                            'D': "Disabling root login doesn't automatically enable "
                                                                 '2FA.'}}],
    'Week 1 - Intro to Cyber Security': [   {   'correct': 'B',
                                                'explanation': 'The In-class Practical Exam (multiple choice, multiple '
                                                               'answer) is worth 40%. The 2 x Portfolios are worth '
                                                               '60%.',
                                                'options': {'A': '60%', 'B': '40%', 'C': '50%', 'D': '30%'},
                                                'question': 'What percentage of the overall grade is the In-class '
                                                            'Practical Exam worth?',
                                                'wrong_explanations': {   'A': '60% is the weight of the portfolios.',
                                                                          'C': '50/50 is not the split — it is 60/40.',
                                                                          'D': '30% is not correct for any '
                                                                               'assessment.'}},
                                            {   'correct': 'C',
                                                'explanation': 'Kali Linux is the dedicated attacker VM. It is '
                                                               'pre-loaded with security and penetration testing '
                                                               'tools.',
                                                'options': {   'A': 'Ubuntu Server',
                                                               'B': 'Windows 10',
                                                               'C': 'Kali Linux',
                                                               'D': 'OWASP Juice Shop'},
                                                'question': "Which Virtual Machine is used as the 'attacker' machine "
                                                            'in the labs?',
                                                'wrong_explanations': {   'A': 'Ubuntu Server is the target VM running '
                                                                               'WordPress.',
                                                                          'B': 'Windows 10 is not part of the lab '
                                                                               'environment.',
                                                                          'D': 'OWASP Juice Shop is a vulnerable web '
                                                                               'application, not an OS.'}},
                                            {   'correct': 'D',
                                                'explanation': 'UTM is recommended for Apple M-series Macs because '
                                                               'VirtualBox does not fully support ARM64 architecture.',
                                                'options': {   'A': 'VirtualBox',
                                                               'B': 'VMware Fusion',
                                                               'C': 'Hyper-V',
                                                               'D': 'UTM'},
                                                'question': 'Which hypervisor is recommended for macOS M-series '
                                                            '(ARM64) users?',
                                                'wrong_explanations': {   'A': 'VirtualBox works on Intel Macs and '
                                                                               'Windows/Linux but not all VMs run on '
                                                                               'Apple Silicon.',
                                                                          'B': 'VMware Fusion is not mentioned in the '
                                                                               'course materials.',
                                                                          'C': 'Hyper-V is Windows-only.'}},
                                            {   'correct': 'B',
                                                'explanation': 'LO2: Understand, analyse and practically apply the '
                                                               'security properties of confidentiality, integrity, and '
                                                               'availability through the use of cryptographic '
                                                               'primitives.',
                                                'options': {'A': 'LO1', 'B': 'LO2', 'C': 'LO3', 'D': 'LO4'},
                                                'question': "Which Learning Outcome covers 'applying confidentiality, "
                                                            'integrity, and availability through cryptographic '
                                                            "primitives'?",
                                                'wrong_explanations': {   'A': 'LO1 is about preventing/mitigating '
                                                                               'cyber-crime.',
                                                                          'C': 'LO3 is about evaluating privacy and '
                                                                               'anonymity risks.',
                                                                          'D': 'There is no LO4 on this module.'}},
                                            {   'correct': 'C',
                                                'explanation': 'Availability ensures data and systems are accessible '
                                                               'when needed. Backups protect against data loss, '
                                                               'directly supporting availability.',
                                                'options': {   'A': 'Confidentiality',
                                                               'B': 'Non-repudiation',
                                                               'C': 'Availability',
                                                               'D': 'Integrity'},
                                                'question': 'What cybersecurity fundamental principle justifies '
                                                            'backing up your work?',
                                                'wrong_explanations': {   'A': 'Confidentiality is about keeping data '
                                                                               'secret.',
                                                                          'B': 'Non-repudiation proves an action '
                                                                               'occurred.',
                                                                          'D': 'Integrity ensures data has not been '
                                                                               'tampered with.'}},
                                            {   'correct': 'C',
                                                'explanation': 'Portfolio marks are 65% task completion mark plus 35% '
                                                               "discretionary 'Wow Factor' mark for additional "
                                                               'learning beyond the brief.',
                                                'options': {   'A': '100% task completion',
                                                               'B': '50% task + 50% Wow Factor',
                                                               'C': '65% task completion + 35% Wow Factor',
                                                               'D': '80% task + 20% presentation'},
                                                'question': 'How are Portfolio marks structured on this module?',
                                                'wrong_explanations': {   'A': 'There is a Wow Factor component on top '
                                                                               'of task completion.',
                                                                          'B': 'The split is 65/35, not 50/50.',
                                                                          'D': '80/20 is not the stated structure.'}},
                                            {   'correct': 'C',
                                                'explanation': 'The Wow Factor encourages increasingly higher '
                                                               'standards, individual creativity, inquisitiveness, '
                                                               'independence, ownership, and deep engagement. It is '
                                                               'optional.',
                                                'options': {   'A': 'Group work and collaboration — group work is '
                                                                    'encouraged generally but the Wow Factor is '
                                                                    'individual',
                                                               'B': 'Copying best examples from classmates — if others '
                                                                    'do the same Wow Factor submission, it is no '
                                                                    'longer considered Wow Factor',
                                                               'C': 'Individual creativity, inquisitiveness, and deep '
                                                                    'engagement',
                                                               'D': 'Memorisation of lecture slides — memorisation is '
                                                                    'not the aim — deep engagement and creativity are'},
                                                'question': 'What is the Wow Factor designed to encourage?',
                                                'wrong_explanations': {   'A': 'Group work is encouraged generally but '
                                                                               'the Wow Factor is individual.',
                                                                          'B': 'If others do the same Wow Factor '
                                                                               'submission, it is no longer considered '
                                                                               'Wow Factor.',
                                                                          'D': 'Memorisation is not the aim — deep '
                                                                               'engagement and creativity are.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The course suggests using an outliner tool like '
                                                               'Dynalist or a note-taking app like Obsidian, or '
                                                               'capturing notes on a private GitHub repo.',
                                                'options': {   'A': 'Microsoft Word',
                                                               'B': 'Obsidian or Dynalist',
                                                               'C': 'Google Sheets',
                                                               'D': 'Notepad'},
                                                'question': 'Which tool is suggested for taking and maintaining '
                                                            'detailed notes on this module?',
                                                'wrong_explanations': {   'A': 'Microsoft Word is not specifically '
                                                                               'recommended.',
                                                                          'C': 'Google Sheets is a spreadsheet tool, '
                                                                               'not a note-taking app.',
                                                                          'D': 'Notepad lacks the features needed for '
                                                                               'structured note-taking.'}},
                                            {   'correct': 'C',
                                                'explanation': 'OWASP Juice Shop is a deliberately insecure web '
                                                               'application designed for security training. It '
                                                               'simulates real vulnerabilities in a safe, controlled '
                                                               'environment.',
                                                'options': {   'A': 'WordPress',
                                                               'B': 'Ubuntu Server',
                                                               'C': 'OWASP Juice Shop',
                                                               'D': 'Zabbix'},
                                                'question': 'Which deliberate vulnerability platform is used in the '
                                                            'labs to practice web application security?',
                                                'wrong_explanations': {   'A': 'WordPress is used as the target for '
                                                                               'WPScan lab, not as a deliberate '
                                                                               'vulnerability platform.',
                                                                          'B': 'Ubuntu Server is the host OS for the '
                                                                               'target VMs.',
                                                                          'D': 'Zabbix is a monitoring platform.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The module uses a Studio work culture that is Problem '
                                                               'and Project Centred, Experiential, Collaborative, and '
                                                               'focused on Discover & Share.',
                                                'options': {   'A': 'Lecture-based passive learning — the module is '
                                                                    'explicitly not passive — it is hands-on and '
                                                                    'experiential',
                                                               'B': 'Studio work, problem and project centred, '
                                                                    'experiential',
                                                               'C': 'Textbook reading and written exams only — the '
                                                                    'module includes practical labs, not just written '
                                                                    'assessments',
                                                               'D': 'Online-only self-paced learning — the module '
                                                                    'includes in-person labs and collaboration'},
                                                'question': 'What learning style best describes the approach of this '
                                                            'cyber security module?',
                                                'wrong_explanations': {   'A': 'The module is explicitly not passive — '
                                                                               'it is hands-on and experiential.',
                                                                          'C': 'The module includes practical labs, '
                                                                               'not just written assessments.',
                                                                          'D': 'The module includes in-person labs and '
                                                                               'collaboration.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The CIA Triad — Confidentiality (data kept secret), '
                                                               'Integrity (data accurate and untampered), Availability '
                                                               '(data accessible when needed) — is the cornerstone '
                                                               'security model taught from Week 1.',
                                                'options': {   'A': 'Confidentiality, Identification, Access',
                                                               'B': 'Confidentiality, Integrity, Availability',
                                                               'C': 'Control, Integrity, Authentication',
                                                               'D': 'Cybersecurity, Intelligence, Authorisation'},
                                                'question': 'What are the three pillars of the CIA Triad?',
                                                'wrong_explanations': {   'A': 'Identification and Access are part of '
                                                                               'access control models, not the CIA '
                                                                               'Triad.',
                                                                          'C': 'Control and Authentication are '
                                                                               'security concepts but not the CIA '
                                                                               'Triad.',
                                                                          'D': 'These are not the correct CIA Triad '
                                                                               'terms.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A threat actor is any entity — individual, group, '
                                                               'nation-state — that has the intent and capability to '
                                                               'exploit vulnerabilities and cause harm to information '
                                                               'systems.',
                                                'options': {   'A': 'A software tool used to detect intrusions — that '
                                                                    'describes an Intrusion Detection System (IDS)',
                                                               'B': 'Any individual or group that poses a risk to '
                                                                    'systems or data by exploiting vulnerabilities',
                                                               'C': 'A firewall rule that blocks suspicious traffic — '
                                                                    'that describes a firewall rule',
                                                               'D': 'An audit log entry recording suspicious activity '
                                                                    '— that describes an audit log event, not a threat '
                                                                    'actor'},
                                                'question': "Which of the following best describes a 'threat actor' in "
                                                            'cybersecurity?',
                                                'wrong_explanations': {   'A': 'That describes an Intrusion Detection '
                                                                               'System (IDS).',
                                                                          'C': 'That describes a firewall rule.',
                                                                          'D': 'That describes an audit log event, not '
                                                                               'a threat actor.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A vulnerability is a flaw or weakness in a system. An '
                                                               'exploit is the code, tool, or technique that takes '
                                                               'advantage of that vulnerability to cause harm. Not all '
                                                               'vulnerabilities are exploited.',
                                                'options': {   'A': 'They are the same thing — they are distinct '
                                                                    'concepts — one is a weakness, the other is the '
                                                                    'action that abuses it',
                                                               'B': 'A vulnerability is a weakness; an exploit is code '
                                                                    'or technique that takes advantage of that '
                                                                    'weakness',
                                                               'C': 'A vulnerability is an attack; an exploit is a '
                                                                    'defence — both are offensive concepts — neither '
                                                                    'is a defence',
                                                               'D': 'A vulnerability is hardware-based; an exploit is '
                                                                    'software-based — vulnerabilities and exploits '
                                                                    'exist in both hardware and software'},
                                                'question': "What is the difference between a 'vulnerability' and an "
                                                            "'exploit'?",
                                                'wrong_explanations': {   'A': 'They are distinct concepts — one is a '
                                                                               'weakness, the other is the action that '
                                                                               'abuses it.',
                                                                          'C': 'Both are offensive concepts — neither '
                                                                               'is a defence.',
                                                                          'D': 'Vulnerabilities and exploits exist in '
                                                                               'both hardware and software.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Defence in Depth uses multiple layers of security '
                                                               'controls — perimeter, network, host, application, data '
                                                               '— so that a failure in one layer does not expose the '
                                                               'entire system.',
                                                'options': {   'A': 'Using one very strong security control to protect '
                                                                    'all assets — relying on a single control is a '
                                                                    'single point of failure — the opposite of Defence '
                                                                    'in Depth',
                                                               'B': 'Layering multiple security controls so that if '
                                                                    'one fails, others still protect the asset',
                                                               'C': 'Defending only the network perimeter — '
                                                                    'perimeter-only defence leaves internal systems '
                                                                    'unprotected once the perimeter is breached',
                                                               'D': 'Hiring more security staff — staffing levels do '
                                                                    'not define Defence in Depth'},
                                                'question': "Which of these best describes 'Defence in Depth'?",
                                                'wrong_explanations': {   'A': 'Relying on a single control is a '
                                                                               'single point of failure — the opposite '
                                                                               'of Defence in Depth.',
                                                                          'C': 'Perimeter-only defence leaves internal '
                                                                               'systems unprotected once the perimeter '
                                                                               'is breached.',
                                                                          'D': 'Staffing levels do not define Defence '
                                                                               'in Depth.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Black hat hackers operate illegally and maliciously — '
                                                               'breaking into systems for financial gain, data theft, '
                                                               'espionage, or disruption without authorisation.',
                                                'options': {   'A': 'A security researcher hired by a company to test '
                                                                    'its defences — a hacker hired by a company to '
                                                                    "test defences is a 'white hat' or ethical hacker",
                                                               'B': 'A malicious hacker who breaks into systems '
                                                                    'without permission for personal gain or harm',
                                                               'C': 'A government cybersecurity agent — government '
                                                                    'agents may be white hat or state-sponsored — not '
                                                                    'defined as black hat',
                                                               'D': 'A hacker who discloses vulnerabilities '
                                                                    'responsibly — responsible disclosure is a white '
                                                                    'hat practice'},
                                                'question': "What is a 'black hat' hacker?",
                                                'wrong_explanations': {   'A': 'A hacker hired by a company to test '
                                                                               "defences is a 'white hat' or ethical "
                                                                               'hacker.',
                                                                          'C': 'Government agents may be white hat or '
                                                                               'state-sponsored — not defined as black '
                                                                               'hat.',
                                                                          'D': 'Responsible disclosure is a white hat '
                                                                               'practice.'}},
                                            {   'correct': 'B',
                                                'explanation': 'White hat hackers (ethical hackers) are authorised '
                                                               'professionals who test systems with permission to '
                                                               'identify vulnerabilities before malicious actors do — '
                                                               'their work improves security.',
                                                'options': {   'A': 'A hacker who attacks systems purely for fame — '
                                                                    'hacking for fame without permission is black or '
                                                                    'grey hat behaviour',
                                                               'B': 'An authorised security professional who uses '
                                                                    'hacking techniques to find and fix '
                                                                    'vulnerabilities with permission',
                                                               'C': 'A hacker who only attacks government systems — '
                                                                    'white hat hackers work across all sectors, not '
                                                                    'just government',
                                                               'D': 'A beginner hacker with no real skills — skill '
                                                                    "level doesn't define hat colour — authorisation "
                                                                    'does'},
                                                'question': "What is a 'white hat' hacker?",
                                                'wrong_explanations': {   'A': 'Hacking for fame without permission is '
                                                                               'black or grey hat behaviour.',
                                                                          'C': 'White hat hackers work across all '
                                                                               'sectors, not just government.',
                                                                          'D': "Skill level doesn't define hat colour "
                                                                               '— authorisation does.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Grey hat hackers operate without authorisation but '
                                                               'typically do not have malicious intent — they may '
                                                               'expose vulnerabilities publicly or inform the owner, '
                                                               'but the unauthorised access itself is still illegal.',
                                                'options': {   'A': 'A hacker who works exclusively in grey areas of '
                                                                    'the law regarding data — grey hat refers to the '
                                                                    'ethics of the activity, not the legal grey area '
                                                                    'of data',
                                                               'B': 'Someone who breaks into systems without '
                                                                    'permission but without malicious intent — often '
                                                                    'disclosing the vulnerability afterward',
                                                               'C': 'A retired black hat hacker turned security '
                                                                    'consultant — retirement from black hat activities '
                                                                    "doesn't define grey hat",
                                                               'D': 'A hacker who only attacks criminal organisations '
                                                                    '— hacking criminal organisations is still hacking '
                                                                    'without authorisation'},
                                                'question': "What is a 'grey hat' hacker?",
                                                'wrong_explanations': {   'A': 'Grey hat refers to the ethics of the '
                                                                               'activity, not the legal grey area of '
                                                                               'data.',
                                                                          'C': 'Retirement from black hat activities '
                                                                               "doesn't define grey hat.",
                                                                          'D': 'Hacking criminal organisations is '
                                                                               'still hacking without authorisation.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Script kiddies lack technical skills and use '
                                                               'ready-made tools/exploits without deep understanding. '
                                                               'Despite limited skill, they can still cause '
                                                               'significant damage using powerful tools written by '
                                                               'others.',
                                                'options': {   'A': 'A child learning to code in school — a child '
                                                                    'learning to code is a student, not a script '
                                                                    'kiddie',
                                                               'B': 'An inexperienced attacker who uses pre-written '
                                                                    'tools and scripts without understanding how they '
                                                                    'work',
                                                               'C': 'A professional penetration tester who writes '
                                                                    'custom exploits — custom exploit developers are '
                                                                    'sophisticated threat actors, not script kiddies',
                                                               'D': 'A developer who writes malware for hire — '
                                                                    'malware-for-hire developers are highly skilled — '
                                                                    'the opposite of a script kiddie'},
                                                'question': "What is a 'script kiddie'?",
                                                'wrong_explanations': {   'A': 'A child learning to code is a student, '
                                                                               'not a script kiddie.',
                                                                          'C': 'Custom exploit developers are '
                                                                               'sophisticated threat actors, not '
                                                                               'script kiddies.',
                                                                          'D': 'Malware-for-hire developers are highly '
                                                                               'skilled — the opposite of a script '
                                                                               'kiddie.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Nation-state attackers are government-sponsored groups '
                                                               '(e.g., APT28/Russia, Lazarus Group/North Korea) with '
                                                               'significant resources, conducting espionage, sabotage, '
                                                               'or influence operations.',
                                                'options': {   'A': 'A cybercriminal operating within one country only '
                                                                    '— cybercriminals within one country are not '
                                                                    'state-sponsored nation-state actors',
                                                               'B': 'A government-sponsored hacker or group conducting '
                                                                    'cyber operations for political, military, or '
                                                                    'espionage purposes',
                                                               'C': 'A hacker who targets only national infrastructure '
                                                                    '— nation-state actors target many types of '
                                                                    'organisations, not only national infrastructure',
                                                               'D': 'A security researcher employed by a national '
                                                                    'university — university researchers are '
                                                                    'academics, not nation-state actors'},
                                                'question': "What is a 'nation-state' attacker?",
                                                'wrong_explanations': {   'A': 'Cybercriminals within one country are '
                                                                               'not state-sponsored nation-state '
                                                                               'actors.',
                                                                          'C': 'Nation-state actors target many types '
                                                                               'of organisations, not only national '
                                                                               'infrastructure.',
                                                                          'D': 'University researchers are academics, '
                                                                               'not nation-state actors.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Social engineering exploits human psychology rather '
                                                               'than technical vulnerabilities — tricking people into '
                                                               'giving up passwords, clicking malicious links, or '
                                                               'granting access through deception, urgency, or '
                                                               'authority.',
                                                'options': {   'A': 'Hacking social media platforms — hacking social '
                                                                    'platforms is a technical attack — social '
                                                                    'engineering manipulates people',
                                                               'B': 'Psychologically manipulating people into '
                                                                    'revealing confidential information or performing '
                                                                    'actions that compromise security',
                                                               'C': 'Designing security-aware workplace cultures — '
                                                                    'building security culture is security awareness '
                                                                    'training, not social engineering',
                                                               'D': 'Engineering social media algorithms — social '
                                                                    'media algorithms are a technology concept '
                                                                    'unrelated to cybersecurity social engineering'},
                                                'question': "What is 'social engineering' in cybersecurity?",
                                                'wrong_explanations': {   'A': 'Hacking social platforms is a '
                                                                               'technical attack — social engineering '
                                                                               'manipulates people.',
                                                                          'C': 'Building security culture is security '
                                                                               'awareness training, not social '
                                                                               'engineering.',
                                                                          'D': 'Social media algorithms are a '
                                                                               'technology concept unrelated to '
                                                                               'cybersecurity social engineering.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Vishing (voice phishing) uses phone calls — the '
                                                               'attacker impersonates a bank, tech support, or '
                                                               'authority figure to trick the victim into revealing '
                                                               'sensitive information or transferring money.',
                                                'options': {   'A': 'Phishing via video call — video call phishing is '
                                                                    "sometimes called 'deepfake phishing' — vishing "
                                                                    'specifically uses voice/phone',
                                                               'B': 'Voice phishing — using phone calls to trick '
                                                                    'victims into revealing personal or financial '
                                                                    'information',
                                                               'C': 'Visual phishing using fake websites — fake '
                                                                    'websites are standard phishing — vishing is '
                                                                    'voice-based',
                                                               'D': 'Phishing targeting executives (VIPs) — targeting '
                                                                    "executives is 'whale phishing' or 'whaling'"},
                                                'question': "What is 'vishing'?",
                                                'wrong_explanations': {   'A': 'Video call phishing is sometimes '
                                                                               "called 'deepfake phishing' — vishing "
                                                                               'specifically uses voice/phone.',
                                                                          'C': 'Fake websites are standard phishing — '
                                                                               'vishing is voice-based.',
                                                                          'D': "Targeting executives is 'whale "
                                                                               "phishing' or 'whaling'."}},
                                            {   'correct': 'B',
                                                'explanation': 'Smishing (SMS phishing) sends fraudulent text messages '
                                                               'with malicious links or requests — often pretending to '
                                                               'be a delivery company, bank, or government agency.',
                                                'options': {   'A': 'Phishing via social media',
                                                               'B': 'Phishing via SMS text messages',
                                                               'C': 'Phishing via email',
                                                               'D': 'Phishing via phone calls'},
                                                'question': "What is 'smishing'?",
                                                'wrong_explanations': {   'A': 'Phishing via social media is sometimes '
                                                                               "called 'angler phishing'.",
                                                                          'C': 'Email phishing is simply called '
                                                                               "'phishing'.",
                                                                          'D': "Phone call phishing is 'vishing'."}},
                                            {   'correct': 'B',
                                                'explanation': 'Pretexting involves inventing a believable scenario — '
                                                               'e.g., posing as an IT helpdesk technician, auditor, or '
                                                               'new employee — to gain trust and extract information '
                                                               'or access.',
                                                'options': {   'A': 'Sending a text message before a phone call to '
                                                                    'build trust — sending texts before calls is not '
                                                                    'pretexting — pretexting is about creating false '
                                                                    'scenarios',
                                                               'B': 'Creating a fabricated scenario (pretext) to '
                                                                    'manipulate a victim into providing information or '
                                                                    'access',
                                                               'C': 'Adding false metadata to emails to bypass spam '
                                                                    'filters — email metadata manipulation is a '
                                                                    'technical evasion technique, not pretexting',
                                                               'D': 'Using pre-written scripts for phishing attacks — '
                                                                    'pre-written scripts are a tool — pretexting is '
                                                                    'the scenario-building technique'},
                                                'question': "What is 'pretexting' as a social engineering technique?",
                                                'wrong_explanations': {   'A': 'Sending texts before calls is not '
                                                                               'pretexting — pretexting is about '
                                                                               'creating false scenarios.',
                                                                          'C': 'Email metadata manipulation is a '
                                                                               'technical evasion technique, not '
                                                                               'pretexting.',
                                                                          'D': 'Pre-written scripts are a tool — '
                                                                               'pretexting is the scenario-building '
                                                                               'technique.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Tailgating exploits social courtesy — an attacker '
                                                               'follows closely behind an authorised person through a '
                                                               'secure door, relying on the person holding it open '
                                                               'rather than authenticating separately.',
                                                'options': {   'A': "Following someone's internet traffic to steal "
                                                                    'credentials — following internet traffic is a '
                                                                    'network interception attack, not tailgating',
                                                               'B': 'Physically following an authorised person through '
                                                                    'a secure door without using your own credentials',
                                                               'C': "Using someone else's session cookie to gain "
                                                                    'access — using a stolen session cookie is session '
                                                                    'hijacking',
                                                               'D': "Installing a GPS tracker on a target's vehicle — "
                                                                    'gPS tracking is surveillance, not tailgating'},
                                                'question': "What is 'tailgating' (piggybacking) as a physical "
                                                            'security attack?',
                                                'wrong_explanations': {   'A': 'Following internet traffic is a '
                                                                               'network interception attack, not '
                                                                               'tailgating.',
                                                                          'C': 'Using a stolen session cookie is '
                                                                               'session hijacking.',
                                                                          'D': 'GPS tracking is surveillance, not '
                                                                               'tailgating.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A virus attaches to legitimate files/programs and '
                                                               'activates when those files are executed — it requires '
                                                               'human action (running a file) to spread, unlike a worm '
                                                               'which spreads automatically.',
                                                'options': {   'A': 'Malware that replicates across networks without '
                                                                    'human interaction — malware that spreads '
                                                                    'automatically across networks without human '
                                                                    'interaction is a worm',
                                                               'B': 'Malware that attaches itself to legitimate '
                                                                    'programs and spreads when the infected file is '
                                                                    'executed',
                                                               'C': 'Software that monitors user activity and sends '
                                                                    'data to third parties — software that monitors '
                                                                    'and exfiltrates activity is spyware',
                                                               'D': 'A program that encrypts files and demands ransom '
                                                                    '— file-encrypting malware demanding payment is '
                                                                    'ransomware'},
                                                'question': 'What is a computer virus?',
                                                'wrong_explanations': {   'A': 'Malware that spreads automatically '
                                                                               'across networks without human '
                                                                               'interaction is a worm.',
                                                                          'C': 'Software that monitors and exfiltrates '
                                                                               'activity is spyware.',
                                                                          'D': 'File-encrypting malware demanding '
                                                                               'payment is ransomware.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Worms spread automatically by exploiting network '
                                                               'vulnerabilities or system weaknesses — no user '
                                                               'interaction needed. Famous examples: WannaCry used a '
                                                               'worm component to spread across networks.',
                                                'options': {   'A': 'Malware that disguises itself as legitimate '
                                                                    'software — malware disguised as legitimate '
                                                                    'software is a Trojan horse',
                                                               'B': 'Malware that self-replicates and spreads '
                                                                    'automatically across networks without requiring '
                                                                    'user action',
                                                               'C': 'A program that attaches to legitimate files and '
                                                                    'spreads when executed — attaching to files and '
                                                                    'requiring execution is a virus',
                                                               'D': 'Software that shows unwanted advertisements — '
                                                                    'showing unwanted ads is adware'},
                                                'question': 'What is a computer worm?',
                                                'wrong_explanations': {   'A': 'Malware disguised as legitimate '
                                                                               'software is a Trojan horse.',
                                                                          'C': 'Attaching to files and requiring '
                                                                               'execution is a virus.',
                                                                          'D': 'Showing unwanted ads is adware.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Like the mythological Trojan horse, this malware '
                                                               'appears legitimate (game, utility, software crack) but '
                                                               'executes malicious code once installed — creating '
                                                               'backdoors, stealing data, or downloading more malware.',
                                                'options': {   'A': 'An attack exploiting a wooden horse emoji in '
                                                                    'messaging apps — the name comes from Greek '
                                                                    'mythology, not messaging apps',
                                                               'B': 'Malware that disguises itself as legitimate '
                                                                    'software to trick users into installing it, then '
                                                                    'performs malicious actions',
                                                               'C': 'A self-replicating program that spreads via email '
                                                                    '— self-replicating email malware is a worm or '
                                                                    'virus',
                                                               'D': 'A vulnerability in the SSH protocol — trojan has '
                                                                    "nothing to do with SSH — it's a malware category"},
                                                'question': 'What is a Trojan horse in cybersecurity?',
                                                'wrong_explanations': {   'A': 'The name comes from Greek mythology, '
                                                                               'not messaging apps.',
                                                                          'C': 'Self-replicating email malware is a '
                                                                               'worm or virus.',
                                                                          'D': 'Trojan has nothing to do with SSH — '
                                                                               "it's a malware category."}},
                                            {   'correct': 'B',
                                                'explanation': 'Rootkits hide malicious activity by intercepting '
                                                               'system calls and manipulating what the OS reports — '
                                                               'making it difficult to detect the infection using '
                                                               'standard tools.',
                                                'options': {   'A': 'A tool used to gain root access via SSH — root '
                                                                    'access via SSH is a legitimate admin function — a '
                                                                    'rootkit is malware',
                                                               'B': 'Malware designed to hide its presence (and other '
                                                                    'malware) from the operating system and security '
                                                                    'tools',
                                                               'C': 'A collection of scanning tools for penetration '
                                                                    'testing — penetration testing toolkits are '
                                                                    'legitimate security tools',
                                                               'D': 'A type of keylogger that records root user '
                                                                    'passwords — a keylogger records keystrokes — a '
                                                                    'rootkit hides malware presence'},
                                                'question': 'What is a rootkit?',
                                                'wrong_explanations': {   'A': 'Root access via SSH is a legitimate '
                                                                               'admin function — a rootkit is malware.',
                                                                          'C': 'Penetration testing toolkits are '
                                                                               'legitimate security tools.',
                                                                          'D': 'A keylogger records keystrokes — a '
                                                                               'rootkit hides malware presence.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Spyware secretly collects and transmits user data — '
                                                               'browsing habits, keystrokes, credentials, and personal '
                                                               "information — to an attacker without the user's "
                                                               'knowledge.',
                                                'options': {   'A': 'Software used by intelligence agencies to monitor '
                                                                    'communications — intelligence agency tools are a '
                                                                    'separate category; spyware is malware targeting '
                                                                    'individuals/organisations',
                                                               'B': 'Malware that secretly monitors user activity and '
                                                                    'sends collected data (keystrokes, browsing, '
                                                                    'credentials) to a third party',
                                                               'C': 'A parental control application — parental '
                                                                    'controls are legitimate software with user '
                                                                    'consent',
                                                               'D': 'A network monitoring tool for IT administrators — '
                                                                    'iT network monitoring is authorised and '
                                                                    'transparent — spyware is unauthorised'},
                                                'question': 'What is spyware?',
                                                'wrong_explanations': {   'A': 'Intelligence agency tools are a '
                                                                               'separate category; spyware is malware '
                                                                               'targeting individuals/organisations.',
                                                                          'C': 'Parental controls are legitimate '
                                                                               'software with user consent.',
                                                                          'D': 'IT network monitoring is authorised '
                                                                               'and transparent — spyware is '
                                                                               'unauthorised.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Adware displays intrusive advertisements to generate '
                                                               'revenue for the attacker — often bundled with free '
                                                               'software. While less dangerous than other malware, it '
                                                               'can slow systems and sometimes include spyware '
                                                               'components.',
                                                'options': {   'A': 'Malware used in advertising network attacks — '
                                                                    'adware targets end users with ads, not '
                                                                    'advertising networks',
                                                               'B': 'Software that automatically displays or downloads '
                                                                    'unwanted advertisements — sometimes bundled with '
                                                                    'free software',
                                                               'C': 'A tool for ad-blocking — ad-blockers are '
                                                                    'legitimate tools that prevent adware',
                                                               'D': 'Ransomware targeting advertising agencies — '
                                                                    'ransomware targeting specific sectors is still '
                                                                    'ransomware, not adware'},
                                                'question': 'What is adware?',
                                                'wrong_explanations': {   'A': 'Adware targets end users with ads, not '
                                                                               'advertising networks.',
                                                                          'C': 'Ad-blockers are legitimate tools that '
                                                                               'prevent adware.',
                                                                          'D': 'Ransomware targeting specific sectors '
                                                                               'is still ransomware, not adware.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Keyloggers capture every keystroke — recording '
                                                               'passwords, credit card numbers, and private messages. '
                                                               'They can be software (malware) or hardware (physical '
                                                               'devices plugged between keyboard and PC).',
                                                'options': {   'A': 'A tool that logs all SSH connections to a server '
                                                                    '— sSH connection logging is a legitimate audit '
                                                                    'function — not a keylogger',
                                                               'B': 'Malware or hardware device that records every '
                                                                    'keystroke typed by a user — capturing passwords, '
                                                                    'messages, and sensitive data',
                                                               'C': 'A security tool that monitors for suspicious '
                                                                    'keyboard activity — security monitoring tools '
                                                                    'detect suspicious activity — keyloggers capture '
                                                                    'everything covertly',
                                                               'D': 'A log management system for keyboard access '
                                                                    'events — log management systems record system '
                                                                    'events — not the same as a covert keystroke '
                                                                    'recorder'},
                                                'question': 'What is a keylogger?',
                                                'wrong_explanations': {   'A': 'SSH connection logging is a legitimate '
                                                                               'audit function — not a keylogger.',
                                                                          'C': 'Security monitoring tools detect '
                                                                               'suspicious activity — keyloggers '
                                                                               'capture everything covertly.',
                                                                          'D': 'Log management systems record system '
                                                                               'events — not the same as a covert '
                                                                               'keystroke recorder.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A botnet is a collection of infected machines '
                                                               "('zombies') under the attacker's command-and-control "
                                                               '(C2) server. Used for DDoS attacks, spam campaigns, '
                                                               'cryptocurrency mining, and credential attacks.',
                                                'options': {   'A': 'A network of automated customer service bots — '
                                                                    'customer service bots are legitimate tools — '
                                                                    'botnets are criminal infrastructure',
                                                               'B': 'A network of compromised computers (bots/zombies) '
                                                                    'controlled by an attacker to perform coordinated '
                                                                    'attacks like DDoS, spam, or credential stuffing',
                                                               'C': 'A legitimate cloud computing cluster — cloud '
                                                                    'clusters are legitimate and authorised — botnets '
                                                                    'use compromised machines',
                                                               'D': 'A network of security monitoring sensors — '
                                                                    'security sensors form a legitimate monitoring '
                                                                    'network — not a botnet'},
                                                'question': 'What is a botnet?',
                                                'wrong_explanations': {   'A': 'Customer service bots are legitimate '
                                                                               'tools — botnets are criminal '
                                                                               'infrastructure.',
                                                                          'C': 'Cloud clusters are legitimate and '
                                                                               'authorised — botnets use compromised '
                                                                               'machines.',
                                                                          'D': 'Security sensors form a legitimate '
                                                                               'monitoring network — not a botnet.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The three authentication factors: (1) Something you '
                                                               'KNOW (password, PIN), (2) Something you HAVE (hardware '
                                                               'token, phone), (3) Something you ARE (biometrics — '
                                                               'fingerprint, face). True MFA uses two or more '
                                                               'different factors.',
                                                'options': {   'A': 'Username, password, and email — username, '
                                                                    "password, and email are all 'something you know' "
                                                                    '— one factor',
                                                               'B': 'Something you know, something you have, and '
                                                                    'something you are',
                                                               'C': "PIN, token, and biometric — pIN is 'know', token "
                                                                    "is 'have', biometric is 'are' — but C is an "
                                                                    'example of factors, not the category names',
                                                               'D': 'Password, fingerprint, and security question — '
                                                                    'password and security question are both '
                                                                    "'something you know' — one factor type"},
                                                'question': 'What are the three factors of authentication?',
                                                'wrong_explanations': {   'A': 'Username, password, and email are all '
                                                                               "'something you know' — one factor.",
                                                                          'C': "PIN is 'know', token is 'have', "
                                                                               "biometric is 'are' — but C is an "
                                                                               'example of factors, not the category '
                                                                               'names.',
                                                                          'D': 'Password and security question are '
                                                                               "both 'something you know' — one factor "
                                                                               'type.'}},
                                            {   'correct': 'B',
                                                'explanation': 'MFA requires factors from at least two different '
                                                               'categories (know + have, or know + are) — e.g., '
                                                               'password + SMS code, or PIN + fingerprint. Two '
                                                               "passwords = single factor (both are 'something you "
                                                               "know').",
                                                'options': {   'A': 'Using a very long, complex password — a long '
                                                                    'password is stronger single-factor auth, not MFA',
                                                               'B': 'Requiring a user to provide two or more '
                                                                    'authentication factors from different categories '
                                                                    'to verify identity',
                                                               'C': 'Using multiple usernames to log in — multiple '
                                                                    "usernames is not MFA — it's just multiple "
                                                                    'accounts',
                                                               'D': 'Requiring two passwords for highly sensitive '
                                                                    "accounts — two passwords are both 'something you "
                                                                    "know' — same factor, not MFA"},
                                                'question': 'What is Multi-Factor Authentication (MFA)?',
                                                'wrong_explanations': {   'A': 'A long password is stronger '
                                                                               'single-factor auth, not MFA.',
                                                                          'C': "Multiple usernames is not MFA — it's "
                                                                               'just multiple accounts.',
                                                                          'D': "Two passwords are both 'something you "
                                                                               "know' — same factor, not MFA."}},
                                            {   'correct': 'A',
                                                'explanation': 'Biometric authentication uses unique physical or '
                                                               'behavioural characteristics: fingerprint, face '
                                                               'recognition, iris scan, retina scan, or voice print. '
                                                               "These are the 'something you ARE' authentication "
                                                               'factor.',
                                                'options': {   'A': 'Authentication using biological data unique to '
                                                                    'the individual — fingerprint, face, iris, voice',
                                                               'B': 'Using biological passwords (randomly generated '
                                                                    'from DNA) — dNA-generated passwords are not a '
                                                                    'real authentication concept',
                                                               'C': 'Authentication requiring a blood test — blood '
                                                                    'tests are not used for authentication',
                                                               'D': 'Any authentication method used in hospitals — '
                                                                    'biometrics are used across all sectors, not just '
                                                                    'hospitals'},
                                                'question': 'What is biometric authentication?',
                                                'wrong_explanations': {   'B': 'DNA-generated passwords are not a real '
                                                                               'authentication concept.',
                                                                          'C': 'Blood tests are not used for '
                                                                               'authentication.',
                                                                          'D': 'Biometrics are used across all '
                                                                               'sectors, not just hospitals.'}},
                                            {   'correct': 'B',
                                                'explanation': 'In DAC, the owner of a resource (file, folder) decides '
                                                               'who else can access it — e.g., file permissions in '
                                                               'standard Linux/Windows where owners can share files '
                                                               'with others.',
                                                'options': {   'A': 'The OS determines access based on mandatory '
                                                                    'security labels — oS-enforced mandatory security '
                                                                    'labels describe MAC (Mandatory Access Control)',
                                                               'B': 'Resource owners control access — they can grant '
                                                                    'or restrict access to other users at their '
                                                                    'discretion',
                                                               'C': "Access is granted based on the user's job role — "
                                                                    'role-based access is RBAC (Role-Based Access '
                                                                    'Control)',
                                                               'D': 'All access decisions are made by a central '
                                                                    'security administrator — centralised '
                                                                    'admin-controlled access is more like MAC or a '
                                                                    'specialised enterprise model'},
                                                'question': 'What is Discretionary Access Control (DAC)?',
                                                'wrong_explanations': {   'A': 'OS-enforced mandatory security labels '
                                                                               'describe MAC (Mandatory Access '
                                                                               'Control).',
                                                                          'C': 'Role-based access is RBAC (Role-Based '
                                                                               'Access Control).',
                                                                          'D': 'Centralised admin-controlled access is '
                                                                               'more like MAC or a specialised '
                                                                               'enterprise model.'}},
                                            {   'correct': 'B',
                                                'explanation': 'RBAC assigns permissions to roles, not directly to '
                                                               "individual users. A user's access is determined by "
                                                               'their role(s). This simplifies access management in '
                                                               "organisations — change a role, change all users' "
                                                               'access.',
                                                'options': {   'A': 'Users are given access based on their IP address '
                                                                    '— iP-based access is a network-level control, not '
                                                                    'RBAC',
                                                               'B': 'Access permissions are assigned to roles (e.g., '
                                                                    'Admin, Manager, Staff), and users are assigned to '
                                                                    'those roles',
                                                               'C': 'The resource owner decides who gets access — '
                                                                    'owner-controlled access is DAC',
                                                               'D': 'Access is based on the current time of day — '
                                                                    'time-based access is attribute-based access '
                                                                    'control (ABAC), not RBAC'},
                                                'question': 'What is Role-Based Access Control (RBAC)?',
                                                'wrong_explanations': {   'A': 'IP-based access is a network-level '
                                                                               'control, not RBAC.',
                                                                          'C': 'Owner-controlled access is DAC.',
                                                                          'D': 'Time-based access is attribute-based '
                                                                               'access control (ABAC), not RBAC.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The NIST CSF provides a risk-based approach to '
                                                               'cybersecurity organised into five core functions: '
                                                               'Identify (assets/risks), Protect (safeguards), Detect '
                                                               '(incidents), Respond (response actions), Recover '
                                                               '(restoration).',
                                                'options': {   'A': 'A list of all known CVEs and their patches — cVE '
                                                                    'lists are maintained separately by MITRE/NVD — '
                                                                    'not the NIST CSF',
                                                               'B': 'A voluntary framework of standards, guidelines, '
                                                                    'and best practices organised around five '
                                                                    'functions: Identify, Protect, Detect, Respond, '
                                                                    'Recover',
                                                               'C': 'Legal requirements for US government '
                                                                    'cybersecurity — the CSF is voluntary for most '
                                                                    'organisations — mandatory requirements come from '
                                                                    'specific regulations',
                                                               'D': 'A certification programme for ethical hackers — '
                                                                    'ethical hacker certifications include CEH, OSCP — '
                                                                    'not the NIST CSF'},
                                                'question': 'What does the NIST Cybersecurity Framework (CSF) provide?',
                                                'wrong_explanations': {   'A': 'CVE lists are maintained separately by '
                                                                               'MITRE/NVD — not the NIST CSF.',
                                                                          'C': 'The CSF is voluntary for most '
                                                                               'organisations — mandatory requirements '
                                                                               'come from specific regulations.',
                                                                          'D': 'Ethical hacker certifications include '
                                                                               'CEH, OSCP — not the NIST CSF.'}},
                                            {   'correct': 'B',
                                                'explanation': 'ISO 27001 is the internationally recognised standard '
                                                               'for Information Security Management Systems (ISMS). '
                                                               'Organisations can be certified against it to '
                                                               'demonstrate systematic security management.',
                                                'options': {   'A': 'A UK government cyber essentials certification — '
                                                                    'cyber Essentials is a UK government scheme — '
                                                                    'different from ISO 27001',
                                                               'B': 'An international standard for establishing, '
                                                                    'implementing, and maintaining an Information '
                                                                    'Security Management System (ISMS)',
                                                               'C': 'A US legal requirement for data protection — iSO '
                                                                    '27001 is an international voluntary standard, not '
                                                                    'US law',
                                                               'D': 'A technical standard for encryption algorithms — '
                                                                    'encryption standards are covered by separate '
                                                                    'standards like FIPS 140'},
                                                'question': 'What is ISO 27001?',
                                                'wrong_explanations': {   'A': 'Cyber Essentials is a UK government '
                                                                               'scheme — different from ISO 27001.',
                                                                          'C': 'ISO 27001 is an international '
                                                                               'voluntary standard, not US law.',
                                                                          'D': 'Encryption standards are covered by '
                                                                               'separate standards like FIPS 140.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Every incident is an event, but not every event is an '
                                                               'incident. Events include normal logins, port scans, '
                                                               'etc. An incident requires a response because it '
                                                               'affects confidentiality, integrity, or availability.',
                                                'options': {   'A': 'They are the same thing — they have different '
                                                                    'meanings — confusing them leads to poor incident '
                                                                    'response',
                                                               'B': 'An event is any observable occurrence; an '
                                                                    'incident is an event that has negatively impacted '
                                                                    '(or threatens to impact) security',
                                                               'C': 'An event is serious; an incident is minor — '
                                                                    'incidents are typically the more serious '
                                                                    'classification',
                                                               'D': 'Events affect hardware; incidents affect software '
                                                                    '— the event/incident distinction is not hardware '
                                                                    'vs software'},
                                                'question': "What is the difference between a 'security event' and a "
                                                            "'security incident'?",
                                                'wrong_explanations': {   'A': 'They have different meanings — '
                                                                               'confusing them leads to poor incident '
                                                                               'response.',
                                                                          'C': 'Incidents are typically the more '
                                                                               'serious classification.',
                                                                          'D': 'The event/incident distinction is not '
                                                                               'hardware vs software.'}},
                                            {   'correct': 'B',
                                                'explanation': 'NIST SP 800-61 defines four phases: (1) Preparation, '
                                                               '(2) Detection & Analysis, (3) Containment, Eradication '
                                                               '& Recovery, (4) Post-Incident Activity (lessons '
                                                               'learned).',
                                                'options': {   'A': 'Detect, Analyse, Contain, Eradicate — '
                                                                    'detect/Analyse/Contain/Eradicate are individual '
                                                                    'steps within the NIST phases, not the four phases '
                                                                    'themselves',
                                                               'B': 'Preparation → Detection & Analysis → Containment, '
                                                                    'Eradication & Recovery → Post-Incident Activity',
                                                               'C': 'Identify, Protect, Detect, Respond — '
                                                                    'identify/Protect/Detect/Respond are NIST CSF '
                                                                    'functions, not incident response phases',
                                                               'D': 'Plan, Do, Check, Act — plan/Do/Check/Act is the '
                                                                    'PDCA cycle from ISO management standards'},
                                                'question': 'What are the four phases of the NIST Incident Response '
                                                            'Lifecycle?',
                                                'wrong_explanations': {   'A': 'Detect/Analyse/Contain/Eradicate are '
                                                                               'individual steps within the NIST '
                                                                               'phases, not the four phases '
                                                                               'themselves.',
                                                                          'C': 'Identify/Protect/Detect/Respond are '
                                                                               'NIST CSF functions, not incident '
                                                                               'response phases.',
                                                                          'D': 'Plan/Do/Check/Act is the PDCA cycle '
                                                                               'from ISO management standards.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Risk = Threat × Vulnerability × Impact. This means '
                                                               "risk increases when there's a capable threat, an "
                                                               'exploitable vulnerability, and high potential impact. '
                                                               'Many frameworks simplify this to Likelihood × Impact.',
                                                'options': {   'A': 'Risk = Cost × Time — cost and time are not the '
                                                                    'standard risk formula components',
                                                               'B': 'Risk = Threat × Vulnerability × Impact (or '
                                                                    'Likelihood × Impact)',
                                                               'C': 'Risk = Number of vulnerabilities × Attack surface',
                                                               'D': 'Risk = Probability × Cost of breach — probability '
                                                                    '× Cost is a financial risk concept — '
                                                                    'cybersecurity risk adds vulnerability and threat '
                                                                    'factors'},
                                                'question': 'In risk management, what is the basic formula for risk?',
                                                'wrong_explanations': {   'A': 'Cost and time are not the standard '
                                                                               'risk formula components.',
                                                                          'C': 'While related, this is not the '
                                                                               'standard formula.',
                                                                          'D': 'Probability × Cost is a financial risk '
                                                                               'concept — cybersecurity risk adds '
                                                                               'vulnerability and threat factors.'}},
                                            {   'correct': 'C',
                                                'explanation': 'Risk acceptance means management acknowledges the risk '
                                                               'and consciously decides to tolerate it — usually when '
                                                               'mitigation costs are too high relative to the '
                                                               'potential impact or likelihood.',
                                                'options': {   'A': 'Eliminating the vulnerability entirely — '
                                                                    'eliminating the vulnerability is risk avoidance '
                                                                    'or remediation',
                                                               'B': 'Transferring the risk to a third party (e.g., '
                                                                    'insurance) — passing risk to insurance/third '
                                                                    'party is risk transference',
                                                               'C': 'Acknowledging the risk exists and choosing not to '
                                                                    'mitigate it — usually when the cost of mitigation '
                                                                    "exceeds the risk's potential impact",
                                                               'D': 'Reducing the likelihood or impact of the risk — '
                                                                    'reducing likelihood or impact is risk mitigation'},
                                                'question': "What is 'risk acceptance' as a risk management strategy?",
                                                'wrong_explanations': {   'A': 'Eliminating the vulnerability is risk '
                                                                               'avoidance or remediation.',
                                                                          'B': 'Passing risk to insurance/third party '
                                                                               'is risk transference.',
                                                                          'D': 'Reducing likelihood or impact is risk '
                                                                               'mitigation.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The 3-2-1 rule: 3 total copies (original + 2 backups), '
                                                               '2 different media types (e.g., disk + tape), 1 offsite '
                                                               'location — protects against hardware failure, '
                                                               'ransomware, and site disasters.',
                                                'options': {   'A': 'Back up 3 times daily, 2 servers, 1 cloud — '
                                                                    'frequency and server count are not what the 3-2-1 '
                                                                    'rule defines',
                                                               'B': 'Keep 3 copies of data, on 2 different media '
                                                                    'types, with 1 copy offsite',
                                                               'C': '3 employees responsible, 2 backup systems, 1 test '
                                                                    'per year',
                                                               'D': '3 hours RTO, 2 hours RPO, 1 backup location — '
                                                                    'rTO/RPO are recovery objectives — not the 3-2-1 '
                                                                    'backup rule'},
                                                'question': "What is the '3-2-1 backup rule'?",
                                                'wrong_explanations': {   'A': 'Frequency and server count are not '
                                                                               'what the 3-2-1 rule defines.',
                                                                          'C': 'Staff assignments and testing '
                                                                               'frequency are not the 3-2-1 rule.',
                                                                          'D': 'RTO/RPO are recovery objectives — not '
                                                                               'the 3-2-1 backup rule.'}},
                                            {   'correct': 'B',
                                                'explanation': 'OSINT uses publicly available sources — websites, '
                                                               'social media, DNS records, job listings, WHOIS data, '
                                                               'LinkedIn — to gather intelligence about targets. Used '
                                                               'legitimately in security research and by attackers for '
                                                               'reconnaissance.',
                                                'options': {   'A': 'Intelligence gathered by hacking into open-source '
                                                                    "software repositories — oSINT doesn't involve "
                                                                    'hacking — it uses only publicly available '
                                                                    'information',
                                                               'B': 'Collecting and analysing publicly available '
                                                                    'information from the internet, social media, '
                                                                    'public records, and other open sources',
                                                               'C': 'Intelligence shared between open-source security '
                                                                    'communities — community-shared intelligence is '
                                                                    'threat intelligence sharing, not OSINT',
                                                               'D': "A type of vulnerability scan that doesn't require "
                                                                    'authentication — unauthenticated scans are a '
                                                                    'vulnerability scanning technique, not OSINT'},
                                                'question': 'What is OSINT (Open Source Intelligence)?',
                                                'wrong_explanations': {   'A': "OSINT doesn't involve hacking — it "
                                                                               'uses only publicly available '
                                                                               'information.',
                                                                          'C': 'Community-shared intelligence is '
                                                                               'threat intelligence sharing, not '
                                                                               'OSINT.',
                                                                          'D': 'Unauthenticated scans are a '
                                                                               'vulnerability scanning technique, not '
                                                                               'OSINT.'}},
                                            {   'correct': 'B',
                                                'explanation': "Lockheed Martin's Cyber Kill Chain describes 7 stages: "
                                                               '(1) Reconnaissance, (2) Weaponisation, (3) Delivery, '
                                                               '(4) Exploitation, (5) Installation, (6) C2 Command & '
                                                               'Control, (7) Actions on Objectives.',
                                                'options': {   'A': 'A list of all known malware families — malware '
                                                                    'families are catalogued separately — the kill '
                                                                    'chain describes attack stages',
                                                               'B': 'A framework describing the stages of a cyber '
                                                                    'attack: Reconnaissance → Weaponisation → Delivery '
                                                                    '→ Exploitation → Installation → C2 → Actions on '
                                                                    'Objectives',
                                                               'C': 'The legal process for prosecuting cybercriminals '
                                                                    '— legal prosecution is outside the scope of the '
                                                                    'kill chain model',
                                                               'D': 'A supply chain security framework — supply chain '
                                                                    'security is a separate concept from the cyber '
                                                                    'kill chain'},
                                                'question': "What is the 'cyber kill chain'?",
                                                'wrong_explanations': {   'A': 'Malware families are catalogued '
                                                                               'separately — the kill chain describes '
                                                                               'attack stages.',
                                                                          'C': 'Legal prosecution is outside the scope '
                                                                               'of the kill chain model.',
                                                                          'D': 'Supply chain security is a separate '
                                                                               'concept from the cyber kill chain.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Reconnaissance (the first kill chain stage) involves '
                                                               'gathering intelligence about the target — network '
                                                               'topology, employee names, software versions, email '
                                                               'formats — using tools like Nmap, OSINT, and Google '
                                                               'dorking.',
                                                'options': {   'A': 'Recovering systems after a breach — recovering '
                                                                    'systems after a breach is part of incident '
                                                                    'response',
                                                               'B': 'The information-gathering phase where attackers '
                                                                    'research the target — identifying IP ranges, '
                                                                    'employees, software versions, and potential entry '
                                                                    'points',
                                                               'C': 'Installing malware on a target system — '
                                                                    'installing malware is the Installation phase of '
                                                                    'the kill chain',
                                                               'D': 'Communicating with a command-and-control server — '
                                                                    'c2 communication is the Command & Control phase'},
                                                'question': "What is 'reconnaissance' in the context of a cyber "
                                                            'attack?',
                                                'wrong_explanations': {   'A': 'Recovering systems after a breach is '
                                                                               'part of incident response.',
                                                                          'C': 'Installing malware is the Installation '
                                                                               'phase of the kill chain.',
                                                                          'D': 'C2 communication is the Command & '
                                                                               'Control phase.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Patch management ensures systems are kept up to date '
                                                               'with security fixes. Unpatched systems are a leading '
                                                               'cause of breaches — many major attacks exploit '
                                                               'vulnerabilities that had patches available.',
                                                'options': {   'A': 'Stitching together code segments in software '
                                                                    'development — code stitching is a software '
                                                                    'development concept, not patch management',
                                                               'B': 'The systematic process of identifying, acquiring, '
                                                                    'testing, and applying software updates (patches) '
                                                                    'to fix vulnerabilities',
                                                               'C': 'Monitoring network traffic for attack patterns — '
                                                                    'traffic monitoring is network security '
                                                                    'monitoring, not patch management',
                                                               'D': 'Creating backup copies of software before updates '
                                                                    '— backups before updates are part of change '
                                                                    'management, not patch management itself'},
                                                'question': "What does 'patch management' mean in cybersecurity?",
                                                'wrong_explanations': {   'A': 'Code stitching is a software '
                                                                               'development concept, not patch '
                                                                               'management.',
                                                                          'C': 'Traffic monitoring is network security '
                                                                               'monitoring, not patch management.',
                                                                          'D': 'Backups before updates are part of '
                                                                               'change management, not patch '
                                                                               'management itself.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Security awareness training reduces human-factor '
                                                               'vulnerabilities — employees learn to recognise '
                                                               'phishing, use strong passwords, follow policies, and '
                                                               'understand their role in protecting the organisation.',
                                                'options': {   'A': 'Technical training for security engineers — '
                                                                    'technical training for engineers is separate from '
                                                                    'organisation-wide awareness training',
                                                               'B': 'Educating all employees about cybersecurity '
                                                                    'threats, safe practices, and their '
                                                                    'responsibilities — because humans are often the '
                                                                    'weakest link',
                                                               'C': 'Awareness campaigns for customers about product '
                                                                    'security — customer awareness is part of security '
                                                                    'communication, not internal awareness training',
                                                               'D': 'Mandatory government training for IT staff — '
                                                                    'security awareness training is for all staff, not '
                                                                    'just IT'},
                                                'question': "What is 'security awareness training' and why is it "
                                                            'important?',
                                                'wrong_explanations': {   'A': 'Technical training for engineers is '
                                                                               'separate from organisation-wide '
                                                                               'awareness training.',
                                                                          'C': 'Customer awareness is part of security '
                                                                               'communication, not internal awareness '
                                                                               'training.',
                                                                          'D': 'Security awareness training is for all '
                                                                               'staff, not just IT.'}},
                                            {   'correct': 'B',
                                                'explanation': "Zero Trust operates on 'never trust, always verify' — "
                                                               'no user or device is automatically trusted, even '
                                                               'inside the corporate network. Every access request is '
                                                               'authenticated, authorised, and encrypted.',
                                                'options': {   'A': 'A model that trusts no software and uses only '
                                                                    'hardware security — zero Trust is not hardware vs '
                                                                    "software — it's about verification of every "
                                                                    'access request',
                                                               'B': 'A security principle that assumes no user, '
                                                                    'device, or network is inherently trusted — every '
                                                                    'access request must be verified regardless of '
                                                                    'location',
                                                               'C': 'A model that allows zero downtime by eliminating '
                                                                    'security checks — zero Trust increases security '
                                                                    'controls, not reduces them for availability',
                                                               'D': 'A networking model that blocks all external '
                                                                    'traffic by default — blocking all external '
                                                                    'traffic is a firewall rule — Zero Trust goes '
                                                                    'beyond perimeter security'},
                                                'question': "What is a 'zero-trust' security model?",
                                                'wrong_explanations': {   'A': 'Zero Trust is not hardware vs software '
                                                                               "— it's about verification of every "
                                                                               'access request.',
                                                                          'C': 'Zero Trust increases security '
                                                                               'controls, not reduces them for '
                                                                               'availability.',
                                                                          'D': 'Blocking all external traffic is a '
                                                                               'firewall rule — Zero Trust goes beyond '
                                                                               'perimeter security.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A SOC is a 24/7 team using security tools (SIEM, '
                                                               "IDS/IPS) to monitor an organisation's security "
                                                               'posture, detect threats, investigate alerts, and '
                                                               'coordinate incident response.',
                                                'options': {   'A': 'A physical room where computer equipment is '
                                                                    'stored — a physical room for equipment is a data '
                                                                    'centre — not a SOC',
                                                               'B': 'A centralised team responsible for continuously '
                                                                    'monitoring, detecting, and responding to '
                                                                    'cybersecurity threats in real time',
                                                               'C': 'A team that develops security software — security '
                                                                    'software development is done by security '
                                                                    'engineers/developers',
                                                               'D': 'A compliance team that manages GDPR requirements '
                                                                    '— gDPR compliance is managed by Data Protection '
                                                                    'Officers, not typically the SOC'},
                                                'question': "What is the purpose of a 'Security Operations Centre' "
                                                            '(SOC)?',
                                                'wrong_explanations': {   'A': 'A physical room for equipment is a '
                                                                               'data centre — not a SOC.',
                                                                          'C': 'Security software development is done '
                                                                               'by security engineers/developers.',
                                                                          'D': 'GDPR compliance is managed by Data '
                                                                               'Protection Officers, not typically the '
                                                                               'SOC.'}},
                                            {   'correct': 'B',
                                                'explanation': '2FA is a subset of MFA — it requires exactly two '
                                                               'factors from different categories. The most common '
                                                               'implementation is password (something you know) + '
                                                               'SMS/app code (something you have).',
                                                'options': {   'A': 'Using two different passwords to log in — two '
                                                                    "passwords are both 'something you know' — one "
                                                                    'factor type',
                                                               'B': 'A specific implementation of MFA requiring '
                                                                    'exactly two authentication factors from different '
                                                                    'categories',
                                                               'C': 'Authenticating on two separate devices '
                                                                    'simultaneously — authenticating on two devices '
                                                                    'simultaneously is not 2FA',
                                                               'D': 'Two administrators approving access together — '
                                                                    "dual administrator approval is a 'four-eyes "
                                                                    "principle' control — not 2FA"},
                                                'question': "What is 'two-factor authentication' (2FA)?",
                                                'wrong_explanations': {   'A': "Two passwords are both 'something you "
                                                                               "know' — one factor type.",
                                                                          'C': 'Authenticating on two devices '
                                                                               'simultaneously is not 2FA.',
                                                                          'D': 'Dual administrator approval is a '
                                                                               "'four-eyes principle' control — not "
                                                                               '2FA.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Physical security protects the physical environment — '
                                                               'access control (locks, keycards), CCTV, security '
                                                               'guards, server room controls — because physical access '
                                                               'can bypass all digital security controls.',
                                                'options': {   'A': 'Protecting computers from power surges — power '
                                                                    'surge protection is about hardware resilience '
                                                                    '(UPS), not physical security',
                                                               'B': 'Protecting physical access to systems, '
                                                                    'facilities, and equipment to prevent unauthorised '
                                                                    'physical access, theft, or damage',
                                                               'C': 'Using hardware firewalls instead of software '
                                                                    'firewalls — hardware vs software firewalls is a '
                                                                    'network security concept',
                                                               'D': 'The physical layout of network cables — cable '
                                                                    'layout is network infrastructure — physical '
                                                                    'security is about access control'},
                                                'question': "What is 'physical security' in the context of "
                                                            'cybersecurity?',
                                                'wrong_explanations': {   'A': 'Power surge protection is about '
                                                                               'hardware resilience (UPS), not '
                                                                               'physical security.',
                                                                          'C': 'Hardware vs software firewalls is a '
                                                                               'network security concept.',
                                                                          'D': 'Cable layout is network infrastructure '
                                                                               '— physical security is about access '
                                                                               'control.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Password managers enable users to have long, unique, '
                                                               'random passwords for every account (preventing '
                                                               'password reuse) stored in an encrypted vault accessed '
                                                               'by one strong master password.',
                                                'options': {   'A': 'A tool that automatically resets passwords '
                                                                    'periodically — automatic password rotation is a '
                                                                    'separate feature — password managers primarily '
                                                                    'store and generate',
                                                               'B': 'An application that securely stores and generates '
                                                                    'unique, strong passwords for each account — '
                                                                    'allowing users to use complex passwords without '
                                                                    'memorising them',
                                                               'C': 'A browser extension that shows password strength '
                                                                    '— password strength indicators are a UI feature, '
                                                                    'not a password manager',
                                                               'D': 'A company policy document about password '
                                                                    'requirements — password policies are '
                                                                    'organisational documents, not software tools'},
                                                'question': "What is a 'password manager' and why is it recommended?",
                                                'wrong_explanations': {   'A': 'Automatic password rotation is a '
                                                                               'separate feature — password managers '
                                                                               'primarily store and generate.',
                                                                          'C': 'Password strength indicators are a UI '
                                                                               'feature, not a password manager.',
                                                                          'D': 'Password policies are organisational '
                                                                               'documents, not software tools.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Credential stuffing exploits password reuse — if '
                                                               'someone uses the same password across multiple sites, '
                                                               'attackers with breach data from one site can try those '
                                                               'credentials on banking, email, and other accounts.',
                                                'options': {   'A': "Adding fake credentials to a target's database — "
                                                                    'adding fake credentials is database manipulation',
                                                               'B': 'Using large lists of stolen username/password '
                                                                    'pairs from data breaches to attempt automated '
                                                                    'logins on other services, exploiting password '
                                                                    'reuse',
                                                               'C': 'Brute-forcing passwords by trying all '
                                                                    'combinations — trying all combinations is '
                                                                    'brute-force — credential stuffing uses known '
                                                                    'credentials',
                                                               'D': 'Embedding credentials in malware to steal them '
                                                                    'later — malware that steals credentials is a '
                                                                    'credential stealer — not credential stuffing'},
                                                'question': "What is 'credential stuffing'?",
                                                'wrong_explanations': {   'A': 'Adding fake credentials is database '
                                                                               'manipulation.',
                                                                          'C': 'Trying all combinations is brute-force '
                                                                               '— credential stuffing uses known '
                                                                               'credentials.',
                                                                          'D': 'Malware that steals credentials is a '
                                                                               'credential stealer — not credential '
                                                                               'stuffing.'}},
                                            {   'correct': 'B',
                                                'explanation': 'In a MitM attack, the attacker positions themselves '
                                                               'between two communicating parties — intercepting, '
                                                               'reading, and potentially modifying traffic. ARP '
                                                               'poisoning and evil twin Wi-Fi attacks are common MitM '
                                                               'techniques.',
                                                'options': {   'A': 'An insider threat from a mid-level manager — mitM '
                                                                    'has nothing to do with management positions',
                                                               'B': 'An attack where the attacker secretly intercepts '
                                                                    'and relays communications between two parties who '
                                                                    'believe they are communicating directly',
                                                               'C': 'A social engineering attack where the attacker '
                                                                    'impersonates a manager — impersonating authority '
                                                                    'figures is a social engineering/pretexting '
                                                                    'technique',
                                                               'D': 'An attack that injects malicious code into web '
                                                                    'applications — injecting malicious code into web '
                                                                    'apps is XSS or injection attacks'},
                                                'question': "What is a 'man-in-the-middle' (MitM) attack?",
                                                'wrong_explanations': {   'A': 'MitM has nothing to do with management '
                                                                               'positions.',
                                                                          'C': 'Impersonating authority figures is a '
                                                                               'social engineering/pretexting '
                                                                               'technique.',
                                                                          'D': 'Injecting malicious code into web apps '
                                                                               'is XSS or injection attacks.'}},
                                            {   'correct': 'B',
                                                'explanation': 'A data breach is any incident resulting in '
                                                               'unauthorised access to or disclosure of sensitive data '
                                                               '— personal data (GDPR notifiable), financial records, '
                                                               'intellectual property, or confidential business '
                                                               'information.',
                                                'options': {   'A': 'A database performance issue — database '
                                                                    'performance issues are operational concerns, not '
                                                                    'security breaches',
                                                               'B': 'An incident where sensitive, confidential, or '
                                                                    'protected data is accessed, disclosed, or stolen '
                                                                    'without authorisation',
                                                               'C': 'A legal contract violation regarding data sharing '
                                                                    '— contract violations are legal matters — a '
                                                                    'breach in this context is a security incident',
                                                               'D': 'A backup failure that results in data loss — '
                                                                    'backup failures cause data loss but are not data '
                                                                    'breaches — unauthorised access is required'},
                                                'question': "What is a 'data breach'?",
                                                'wrong_explanations': {   'A': 'Database performance issues are '
                                                                               'operational concerns, not security '
                                                                               'breaches.',
                                                                          'C': 'Contract violations are legal matters '
                                                                               '— a breach in this context is a '
                                                                               'security incident.',
                                                                          'D': 'Backup failures cause data loss but '
                                                                               'are not data breaches — unauthorised '
                                                                               'access is required.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Threat intelligence provides actionable information '
                                                               'about threats: who is attacking, their techniques '
                                                               '(TTPs — Tactics, Techniques, Procedures), indicators '
                                                               'of compromise (IoCs), helping defenders prioritise and '
                                                               'respond.',
                                                'options': {   'A': 'Using AI to detect threats automatically — aI '
                                                                    'threat detection is automated security monitoring '
                                                                    '— threat intelligence is knowledge about threats',
                                                               'B': 'Evidence-based knowledge about existing or '
                                                                    'emerging threats — including indicators of '
                                                                    'compromise, attacker TTPs — used to inform '
                                                                    'security decisions',
                                                               'C': 'A database of all known vulnerabilities — cVE '
                                                                    'databases list vulnerabilities — threat '
                                                                    'intelligence includes threat actor information',
                                                               'D': 'Intelligence gathered by hacking threat actor '
                                                                    'groups — hacking threat actors is illegal — '
                                                                    'intelligence is gathered through legitimate '
                                                                    'means'},
                                                'question': "What is 'threat intelligence'?",
                                                'wrong_explanations': {   'A': 'AI threat detection is automated '
                                                                               'security monitoring — threat '
                                                                               'intelligence is knowledge about '
                                                                               'threats.',
                                                                          'C': 'CVE databases list vulnerabilities — '
                                                                               'threat intelligence includes threat '
                                                                               'actor information.',
                                                                          'D': 'Hacking threat actors is illegal — '
                                                                               'intelligence is gathered through '
                                                                               'legitimate means.'}}],
    'Week 11 - Asset Monitoring & Inventory': [   {   'correct': 'B',
                                                      'explanation': 'The three key features are: Asset Identification '
                                                                     'and Classification, Risk Assessment and '
                                                                     'Management, and Incident Response and Recovery.',
                                                      'options': {   'A': 'Firewall Management, Patch Management, '
                                                                          'Incident Response — firewall and Patch '
                                                                          'Management are security controls, not '
                                                                          'inventory management features',
                                                                     'B': 'Asset Identification and Classification, '
                                                                          'Risk Assessment and Management, Incident '
                                                                          'Response and Recovery',
                                                                     'C': 'Network Monitoring, User Authentication, '
                                                                          'Data Encryption — these are general '
                                                                          'security practices, not the specific '
                                                                          'features',
                                                                     'D': 'Threat Intelligence, Vulnerability '
                                                                          'Scanning, Log Analysis — threat '
                                                                          'intelligence and vulnerability scanning are '
                                                                          'distinct security disciplines'},
                                                      'question': 'What are the three key features of cybersecurity '
                                                                  'inventory management?',
                                                      'wrong_explanations': {   'A': 'Firewall and Patch Management '
                                                                                     'are security controls, not '
                                                                                     'inventory management features.',
                                                                                'C': 'These are general security '
                                                                                     'practices, not the specific '
                                                                                     'features.',
                                                                                'D': 'Threat intelligence and '
                                                                                     'vulnerability scanning are '
                                                                                     'distinct security disciplines.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'Asset monitoring is critical for: improved asset '
                                                                     'visibility and utilisation, enhanced security '
                                                                     'and theft prevention, proactive maintenance and '
                                                                     'reduced downtime, better regulatory compliance, '
                                                                     'and data-driven decision-making.',
                                                      'options': {   'A': 'It reduces hardware purchase costs — while '
                                                                          'optimising spending is a benefit, it is not '
                                                                          'the primary cybersecurity reason',
                                                                     'B': 'It provides improved visibility, enhanced '
                                                                          'security, proactive maintenance, better '
                                                                          'compliance, and data-driven decisions',
                                                                     'C': 'It replaces the need for antivirus software '
                                                                          '— asset monitoring complements — it does '
                                                                          'not replace — antivirus and other controls',
                                                                     'D': 'It automatically patches vulnerabilities — '
                                                                          'monitoring detects changes but does not '
                                                                          'automatically patch vulnerabilities'},
                                                      'question': 'Why is Asset Monitoring critical in cybersecurity?',
                                                      'wrong_explanations': {   'A': 'While optimising spending is a '
                                                                                     'benefit, it is not the primary '
                                                                                     'cybersecurity reason.',
                                                                                'C': 'Asset monitoring complements — '
                                                                                     'it does not replace — antivirus '
                                                                                     'and other controls.',
                                                                                'D': 'Monitoring detects changes but '
                                                                                     'does not automatically patch '
                                                                                     'vulnerabilities.'}},
                                                  {   'correct': 'C',
                                                      'explanation': 'The core three-step cycle is: Asset Discovery '
                                                                     'and Inventory → Gap Identification → Automated '
                                                                     'Response. This continuous cycle ensures ongoing '
                                                                     'visibility and security coverage.',
                                                      'options': {   'A': 'Scan → Patch → Report — scan → Patch → '
                                                                          'Report is a simplified vulnerability '
                                                                          'management cycle',
                                                                     'B': 'Identify → Monitor → Respond — identify → '
                                                                          'Monitor → Respond is not the defined cycle '
                                                                          'from the lecture',
                                                                     'C': 'Asset Discovery and Inventory → Gap '
                                                                          'Identification → Automated Response',
                                                                     'D': 'Asset Classification → Risk Rating → '
                                                                          'Remediation — asset Classification → Risk '
                                                                          'Rating → Remediation is a risk management '
                                                                          'cycle'},
                                                      'question': 'What is the core three-step cycle of Cybersecurity '
                                                                  'Asset Inventory Management?',
                                                      'wrong_explanations': {   'A': 'Scan → Patch → Report is a '
                                                                                     'simplified vulnerability '
                                                                                     'management cycle.',
                                                                                'B': 'Identify → Monitor → Respond is '
                                                                                     'not the defined cycle from the '
                                                                                     'lecture.',
                                                                                'D': 'Asset Classification → Risk '
                                                                                     'Rating → Remediation is a risk '
                                                                                     'management cycle.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'The four factors are: (1) Properly identify and '
                                                                     'catalog all assets, (2) Choose the right asset '
                                                                     'monitoring tool, (3) Regularly update asset '
                                                                     'information, (4) Analyse data to optimise asset '
                                                                     'performance and allocation.',
                                                      'options': {   'A': 'Buy tools, hire staff, train users, review '
                                                                          'annually — buy, hire, train, review is not '
                                                                          'the stated four factors',
                                                                     'B': 'Properly identify/catalog assets, choose '
                                                                          'the right tool, regularly update asset '
                                                                          'info, analyse data to optimise',
                                                                     'C': 'Scan daily, patch weekly, report monthly, '
                                                                          'audit annually — scan/patch/report/audit '
                                                                          'describes a security operations cycle, not '
                                                                          'the four factors',
                                                                     'D': 'Identify threats, assess risks, mitigate '
                                                                          'vulnerabilities, monitor compliance — '
                                                                          'identify/assess/mitigate/monitor describes '
                                                                          'risk management, not the four asset '
                                                                          'monitoring factors'},
                                                      'question': 'What are the four factors to consider for '
                                                                  'implementing effective asset monitoring?',
                                                      'wrong_explanations': {   'A': 'Buy, hire, train, review is not '
                                                                                     'the stated four factors.',
                                                                                'C': 'Scan/patch/report/audit '
                                                                                     'describes a security operations '
                                                                                     'cycle, not the four factors.',
                                                                                'D': 'Identify/assess/mitigate/monitor '
                                                                                     'describes risk management, not '
                                                                                     'the four asset monitoring '
                                                                                     'factors.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'Streamlined Incident Response means that having '
                                                                     'a comprehensive, up-to-date asset inventory '
                                                                     'enables security teams to quickly identify which '
                                                                     'systems are affected during an incident and '
                                                                     'respond more effectively.',
                                                      'options': {   'A': 'Incidents are automatically resolved '
                                                                          'without human intervention — human '
                                                                          'intervention is still required — automation '
                                                                          "assists but doesn't replace response",
                                                                     'B': 'A comprehensive asset inventory enables '
                                                                          'faster identification of affected systems '
                                                                          'during an incident',
                                                                     'C': 'Security incidents are reported directly to '
                                                                          'the regulator — asset management does not '
                                                                          'automatically report incidents to '
                                                                          'regulators',
                                                                     'D': 'Incident response teams are replaced by '
                                                                          'automated tools — incident response teams '
                                                                          'are supported by automation, not replaced'},
                                                      'question': "What does 'Streamlined Incident Response' as a "
                                                                  'benefit of asset management mean?',
                                                      'wrong_explanations': {   'A': 'Human intervention is still '
                                                                                     'required — automation assists '
                                                                                     "but doesn't replace response.",
                                                                                'C': 'Asset management does not '
                                                                                     'automatically report incidents '
                                                                                     'to regulators.',
                                                                                'D': 'Incident response teams are '
                                                                                     'supported by automation, not '
                                                                                     'replaced.'}},
                                                  {   'correct': 'B',
                                                      'explanation': "'Enhanced Visibility and Control' provides: a "
                                                                     'real-time view of security posture, visibility '
                                                                     'across the entire network, ability to rapidly '
                                                                     'assess assets and pinpoint coverage gaps, '
                                                                     'continuous asset discovery, and understanding of '
                                                                     'which cybersecurity tools are active.',
                                                      'options': {   'A': 'Cost reduction on hardware purchases — cost '
                                                                          "reduction is 'Provide Cost Optimisation'",
                                                                     'B': "A real-time view of the organisation's "
                                                                          'security posture and visibility across the '
                                                                          'entire network',
                                                                     'C': 'Automatic vulnerability patching — '
                                                                          'automatic patching is not part of this '
                                                                          'benefit',
                                                                     'D': 'Employee activity monitoring — employee '
                                                                          'monitoring is not what this benefit '
                                                                          'describes'},
                                                      'question': "What does 'Enhanced Visibility and Control' as a "
                                                                  'benefit of asset inventory management provide?',
                                                      'wrong_explanations': {   'A': "Cost reduction is 'Provide Cost "
                                                                                     "Optimisation'.",
                                                                                'C': 'Automatic patching is not part '
                                                                                     'of this benefit.',
                                                                                'D': 'Employee monitoring is not what '
                                                                                     'this benefit describes.'}},
                                                  {   'correct': 'C',
                                                      'explanation': 'Assigning risk profiles based on business '
                                                                     'criticality is a key best practice — it ensures '
                                                                     'that the most critical assets receive the '
                                                                     'highest level of protection and priority in '
                                                                     'security planning.',
                                                      'options': {   'A': 'Choose appropriate tools for automated '
                                                                          'discovery',
                                                                     'B': 'Identify all asset types including '
                                                                          'cloud-based assets',
                                                                     'C': 'Assign risk profiles to assets based on '
                                                                          'business criticality',
                                                                     'D': 'Ensure continuous monitoring to detect '
                                                                          'changes'},
                                                      'question': 'Which best practice for asset inventory management '
                                                                  'involves assigning risk profiles based on business '
                                                                  'criticality?',
                                                      'wrong_explanations': {   'A': 'Choosing appropriate tools is a '
                                                                                     'different best practice.',
                                                                                'B': 'Identifying all asset types is a '
                                                                                     'different best practice.',
                                                                                'D': 'Continuous monitoring is a '
                                                                                     'different best practice.'}},
                                                  {   'correct': 'C',
                                                      'explanation': 'Best practices require identifying ALL asset '
                                                                     'types: physical devices (servers, workstations, '
                                                                     'network equipment), software (applications, '
                                                                     'operating systems), and cloud-based assets '
                                                                     '(SaaS, IaaS, PaaS).',
                                                      'options': {   'A': 'Only physical servers and workstations',
                                                                     'B': 'Only software applications — software alone '
                                                                          'is insufficient — physical and cloud assets '
                                                                          'must also be included',
                                                                     'C': 'Physical devices, software, and cloud-based '
                                                                          'assets',
                                                                     'D': 'Only internet-connected devices — '
                                                                          'non-internet-connected assets also pose '
                                                                          'security risks and must be inventoried'},
                                                      'question': 'What types of assets should be identified according '
                                                                  'to best practices for asset inventory management?',
                                                      'wrong_explanations': {   'A': 'Physical servers alone are '
                                                                                     'insufficient — software and '
                                                                                     'cloud assets also matter.',
                                                                                'B': 'Software alone is insufficient — '
                                                                                     'physical and cloud assets must '
                                                                                     'also be included.',
                                                                                'D': 'Non-internet-connected assets '
                                                                                     'also pose security risks and '
                                                                                     'must be inventoried.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'Zabbix is an open-source monitoring platform '
                                                                     'used to track network devices, servers, and '
                                                                     'applications in real-time — supporting asset '
                                                                     'visibility and anomaly detection.',
                                                      'options': {   'A': 'Vulnerability scanning for open ports — '
                                                                          'port scanning is done by Nmap — Zabbix '
                                                                          'monitors running systems',
                                                                     'B': 'Real-time network and infrastructure '
                                                                          'monitoring — tracking asset health, '
                                                                          'availability, and anomalies',
                                                                     'C': 'Penetration testing and exploitation — '
                                                                          'penetration testing uses tools like '
                                                                          'Metasploit or Nmap',
                                                                     'D': 'Encrypting network communications — network '
                                                                          'encryption is handled by TLS/VPNs, not '
                                                                          'Zabbix'},
                                                      'question': 'What is Zabbix used for in cybersecurity contexts?',
                                                      'wrong_explanations': {   'A': 'Port scanning is done by Nmap — '
                                                                                     'Zabbix monitors running systems.',
                                                                                'C': 'Penetration testing uses tools '
                                                                                     'like Metasploit or Nmap.',
                                                                                'D': 'Network encryption is handled by '
                                                                                     'TLS/VPNs, not Zabbix.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'Shadow IT refers to technology deployed by '
                                                                     'employees without official IT approval — these '
                                                                     'assets are invisible to the security team, '
                                                                     'unpatched, and create compliance and security '
                                                                     'risks.',
                                                      'options': {   'A': 'IT systems running on backup power — backup '
                                                                          'power systems (UPS) are a continuity '
                                                                          'concern, not shadow IT',
                                                                     'B': 'Unauthorised hardware or software deployed '
                                                                          "without IT's knowledge, creating unmanaged "
                                                                          'and unsecured assets',
                                                                     'C': 'IT systems that run only at night — '
                                                                          "'Night-only' systems is not a real IT term",
                                                                     'D': 'Dark web monitoring tools used by security '
                                                                          'teams — dark web monitoring is a threat '
                                                                          'intelligence practice, not shadow IT'},
                                                      'question': "What does 'shadow IT' mean and why is it a problem "
                                                                  'for asset inventory management?',
                                                      'wrong_explanations': {   'A': 'Backup power systems (UPS) are a '
                                                                                     'continuity concern, not shadow '
                                                                                     'IT.',
                                                                                'C': "'Night-only' systems is not a "
                                                                                     'real IT term.',
                                                                                'D': 'Dark web monitoring is a threat '
                                                                                     'intelligence practice, not '
                                                                                     'shadow IT.'}},
                                                  {   'correct': 'B',
                                                      'explanation': 'A CMDB stores detailed records of all '
                                                                     'configuration items (CIs) — hardware, software, '
                                                                     'services — and their relationships. It is '
                                                                     'central to asset inventory and ITSM processes.',
                                                      'options': {   'A': 'A database of known malware signatures — '
                                                                          'malware signatures are stored in '
                                                                          'antivirus/EDR databases, not a CMDB',
                                                                     'B': 'A repository that stores information about '
                                                                          'IT assets (configuration items) and their '
                                                                          'relationships',
                                                                     'C': 'A backup system for critical databases — a '
                                                                          'CMDB is a record-keeping system, not a '
                                                                          'backup solution',
                                                                     'D': 'A tool for scanning network vulnerabilities '
                                                                          '— vulnerability scanning is done by tools '
                                                                          'like Nessus — a CMDB stores configuration '
                                                                          'data'},
                                                      'question': 'What is a CMDB (Configuration Management Database)?',
                                                      'wrong_explanations': {   'A': 'Malware signatures are stored in '
                                                                                     'antivirus/EDR databases, not a '
                                                                                     'CMDB.',
                                                                                'C': 'A CMDB is a record-keeping '
                                                                                     'system, not a backup solution.',
                                                                                'D': 'Vulnerability scanning is done '
                                                                                     'by tools like Nessus — a CMDB '
                                                                                     'stores configuration data.'}}],
    'Week 2 - Privacy, Ethics & Legal': [   {   'correct': 'B',
                                                'explanation': "Article 17 of GDPR gives data subjects the 'Right to "
                                                               "Erasure' (also called 'Right to be Forgotten') — they "
                                                               'can request deletion of their personal data.',
                                                'options': {   'A': 'Right to data portability',
                                                               'B': 'Right to erasure',
                                                               'C': 'Right to access',
                                                               'D': 'Right to rectification'},
                                                'question': 'Under GDPR Article 17, what right do data subjects have?',
                                                'wrong_explanations': {   'A': 'Data portability is Article 20.',
                                                                          'C': 'Right of access is Article 15.',
                                                                          'D': 'Right to rectification is Article '
                                                                               '16.'}},
                                            {   'correct': 'B',
                                                'explanation': "The attacker sent a spear-phishing email to the CEO's "
                                                               'EA, disguised as a conference sponsor. The expense '
                                                               'form attachment contained malware that created an '
                                                               'admin account.',
                                                'options': {   'A': 'Exploiting an unpatched server — no server '
                                                                    'exploit was mentioned — it was social engineering',
                                                               'B': 'A spear-phishing email with a malware-laden '
                                                                    'expense form',
                                                               'C': "Brute-forcing the CEO's email — the EA was "
                                                                    'targeted, not the CEO directly',
                                                               'D': 'A man-in-the-middle attack — no MITM attack was '
                                                                    'involved'},
                                                'question': 'In the ransomware case study, how did the attacker gain '
                                                            'initial access?',
                                                'wrong_explanations': {   'A': 'No server exploit was mentioned — it '
                                                                               'was social engineering.',
                                                                          'C': 'The EA was targeted, not the CEO '
                                                                               'directly.',
                                                                          'D': 'No MITM attack was involved.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The Computer Misuse Act 1990 is the primary UK law '
                                                               'making unauthorised computer access a criminal '
                                                               'offence. All lab work was done within a controlled VM '
                                                               'environment in compliance with it.',
                                                'options': {   'A': 'Data Protection Act 2018',
                                                               'B': 'Computer Misuse Act 1990',
                                                               'C': 'Investigatory Powers Act 2016',
                                                               'D': 'NIS Regulations 2018'},
                                                'question': 'Which UK law governs unauthorised computer access and was '
                                                            'referenced in the lab reports?',
                                                'wrong_explanations': {   'A': 'DPA 2018 implements GDPR in the UK — '
                                                                               'it covers data privacy, not computer '
                                                                               'misuse.',
                                                                          'C': 'IPA 2016 covers surveillance powers by '
                                                                               'authorities.',
                                                                          'D': 'NIS Regulations cover '
                                                                               'network/information system security '
                                                                               'for essential services.'}},
                                            {   'correct': 'C',
                                                'explanation': 'A Policy is a concise directive from upper management '
                                                               'that sets a course of action for the entire '
                                                               'organisation. It sits at the top of the IT security '
                                                               'policy hierarchy.',
                                                'options': {   'A': 'Detailed hardware/software usage definitions — '
                                                                    'that describes Standards',
                                                               'B': 'Written instructions for implementing standards — '
                                                                    'that describes Procedures',
                                                               'C': 'A concise directive from upper management that '
                                                                    'sets a course of action',
                                                               'D': 'Recommended actions that can be flexible — that '
                                                                    'describes Guidelines'},
                                                'question': "What is a 'Policy' in the context of IT security?",
                                                'wrong_explanations': {   'A': 'That describes Standards.',
                                                                          'B': 'That describes Procedures.',
                                                                          'D': 'That describes Guidelines.'}},
                                            {   'correct': 'D',
                                                'explanation': 'Policies apply to the entire organisation and sit at '
                                                               'the top of the hierarchy. Below are Standards '
                                                               '(specific to policies), then Procedures and Guidelines '
                                                               '(define usage and implementation).',
                                                'options': {   'A': 'Guidelines',
                                                               'B': 'Procedures',
                                                               'C': 'Standards',
                                                               'D': 'Policies'},
                                                'question': 'In the IT Security Policy Framework hierarchy, what is at '
                                                            'the top?',
                                                'wrong_explanations': {   'A': 'Guidelines are at the bottom — they '
                                                                               'are flexible and recommended, not '
                                                                               'mandatory.',
                                                                          'B': 'Procedures define how to implement '
                                                                               'standards — they are below policies.',
                                                                          'C': 'Standards are specific to a given '
                                                                               'policy — below policies in the '
                                                                               'hierarchy.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Confidential data is owned by the organisation and '
                                                               'includes intellectual property, customer lists, and '
                                                               'patents. It requires strong security controls.',
                                                'options': {   'A': 'Private Data',
                                                               'B': 'Confidential',
                                                               'C': 'Internal Use Only',
                                                               'D': 'Public Domain'},
                                                'question': 'Which data classification category describes information '
                                                            "'owned by the organisation, including intellectual "
                                                            "property and customer lists'?",
                                                'wrong_explanations': {   'A': 'Private Data must be kept private and '
                                                                               'requires compliance controls, but is '
                                                                               'distinct from confidential IP.',
                                                                          'C': 'Internal Use Only is shared internally '
                                                                               'but not externally.',
                                                                          'D': 'Public Domain data is shared with the '
                                                                               'public (e.g., website content).'}},
                                            {   'correct': 'C',
                                                'explanation': 'OFFICIAL is the UK Government classification for '
                                                               'information with a low level of sensitivity used for '
                                                               'routine day-to-day business.',
                                                'options': {   'A': 'TOP SECRET',
                                                               'B': 'SECRET',
                                                               'C': 'OFFICIAL',
                                                               'D': 'CONFIDENTIAL'},
                                                'question': 'Under the UK Government Data Classification Standard, '
                                                            'which classification covers day-to-day business '
                                                            'information with a LOW level of sensitivity?',
                                                'wrong_explanations': {   'A': 'TOP SECRET is used in the US Federal '
                                                                               'classification, not UK Government '
                                                                               'standard.',
                                                                          'B': 'SECRET covers information that would '
                                                                               'cause serious damage to national '
                                                                               'security if disclosed.',
                                                                          'D': 'CONFIDENTIAL is a US Federal '
                                                                               'classification — the UK standard uses '
                                                                               'OFFICIAL, SECRET, and TOP SECRET.'}},
                                            {   'correct': 'B',
                                                'explanation': 'An Acceptable Use Policy defines what actions users '
                                                               'are allowed to perform with IT assets in the User '
                                                               'Domain. It is approved by Upper Management.',
                                                'options': {   'A': 'A policy covering vulnerability assessment '
                                                                    'standards',
                                                               'B': 'A policy defining allowed actions with IT assets '
                                                                    'in the User Domain',
                                                               'C': 'A policy for classifying and protecting critical '
                                                                    'IT assets',
                                                               'D': 'A policy governing security awareness training — '
                                                                    'security awareness training is covered by the '
                                                                    'Security Awareness Policy'},
                                                'question': "What is an 'Acceptable Use Policy' (AUP)?",
                                                'wrong_explanations': {   'A': 'Vulnerability assessment standards are '
                                                                               'covered by the Vulnerability '
                                                                               'Assessment Policy.',
                                                                          'C': 'Asset classification/protection is '
                                                                               'covered by separate Asset '
                                                                               'Classification and Asset Protection '
                                                                               'Policies.',
                                                                          'D': 'Security awareness training is covered '
                                                                               'by the Security Awareness Policy.'}},
                                            {   'correct': 'C',
                                                'explanation': 'Cyberspace lacks authorities functioning like air '
                                                               'traffic controllers. Human behaviour online is often '
                                                               'less mature, and it has become a playground for '
                                                               'cybercriminals — which is why ethics, policy, and '
                                                               'security professionals are essential.',
                                                'options': {   'A': 'Because cyberspace has strong authorities like '
                                                                    'air traffic controllers',
                                                               'B': 'Because human behaviour online is more mature '
                                                                    'than in physical settings',
                                                               'C': 'Because cyberspace lacks central authorities and '
                                                                    'has become a playground for bad actors',
                                                               'D': 'Because all cybercrimes are easily traceable to a '
                                                                    'single jurisdiction'},
                                                'question': 'Why is cybersecurity ethics and policy necessary in '
                                                            'cyberspace?',
                                                'wrong_explanations': {   'A': 'The lecture explicitly states '
                                                                               'cyberspace has NO authorities like air '
                                                                               'traffic controllers.',
                                                                          'B': 'Human behaviour online is described as '
                                                                               'often LESS mature than in normal '
                                                                               'social settings.',
                                                                          'D': 'Jurisdictional complexity is a key '
                                                                               'challenge — cybercrime crosses '
                                                                               'international boundaries.'}},
                                            {   'correct': 'B',
                                                'explanation': 'The UK Government classification standard has three '
                                                               'tiers: OFFICIAL (low sensitivity), SECRET (serious '
                                                               'damage if disclosed), and TOP SECRET (grave damage if '
                                                               'disclosed).',
                                                'options': {   'A': 'Top Secret, Secret, Confidential',
                                                               'B': 'Official, Secret, Top Secret',
                                                               'C': 'Public, Internal, Confidential',
                                                               'D': 'Private, Restricted, Official'},
                                                'question': 'What are the three levels of the UK Government Data '
                                                            'Classification Standard mentioned in the lecture?',
                                                'wrong_explanations': {   'A': 'Top Secret, Secret, Confidential is '
                                                                               'the US Federal Government standard, '
                                                                               'not the UK standard.',
                                                                          'C': 'Public, Internal, Confidential is a '
                                                                               'generic data classification model, not '
                                                                               'the UK Government standard.',
                                                                          'D': 'Private, Restricted, Official is not '
                                                                               'the UK Government standard.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Non-repudiation ensures that a party cannot deny '
                                                               'having performed an action — e.g., a digital signature '
                                                               'proves who sent a message. It is often implemented via '
                                                               'cryptographic techniques.',
                                                'options': {   'A': 'The ability to deny performing an action — '
                                                                    'non-repudiation is the opposite — it prevents '
                                                                    'denial',
                                                               'B': 'The ability to prove that an action was performed '
                                                                    'by a specific party, who cannot later deny it',
                                                               'C': 'Encrypting messages so only the recipient can '
                                                                    'read them — that describes confidentiality via '
                                                                    'encryption',
                                                               'D': 'Blocking users from accessing resources they are '
                                                                    'not authorised for — that describes access '
                                                                    'control / authorisation'},
                                                'question': "What is 'non-repudiation' in information security?",
                                                'wrong_explanations': {   'A': 'Non-repudiation is the opposite — it '
                                                                               'prevents denial.',
                                                                          'C': 'That describes confidentiality via '
                                                                               'encryption.',
                                                                          'D': 'That describes access control / '
                                                                               'authorisation.'}},
                                            {   'correct': 'C',
                                                'explanation': 'A Data Controller decides WHY and HOW personal data is '
                                                               'processed. They bear primary responsibility for GDPR '
                                                               'compliance.',
                                                'options': {   'A': 'The software used to store personal data — '
                                                                    'software is not a legal entity — it cannot be a '
                                                                    'Data Controller',
                                                               'B': 'The individual whose data is being processed — '
                                                                    'the individual whose data is processed is the '
                                                                    "'Data Subject'",
                                                               'C': 'The entity that determines the purposes and means '
                                                                    'of processing personal data',
                                                               'D': 'A government body that audits data breaches — the '
                                                                    'supervisory authority (e.g., the ICO in the UK) '
                                                                    'monitors compliance but is not the Data '
                                                                    'Controller'},
                                                'question': "Under GDPR, what is a 'Data Controller'?",
                                                'wrong_explanations': {   'A': 'Software is not a legal entity — it '
                                                                               'cannot be a Data Controller.',
                                                                          'B': 'The individual whose data is processed '
                                                                               "is the 'Data Subject'.",
                                                                          'D': 'The supervisory authority (e.g., the '
                                                                               'ICO in the UK) monitors compliance but '
                                                                               'is not the Data Controller.'}},
                                            {   'correct': 'C',
                                                'explanation': 'The maximum GDPR fine is €20 million or 4% of the '
                                                               "company's total global annual turnover (whichever is "
                                                               'higher) for the most serious violations.',
                                                'options': {   'A': '€1 million or 1% of global annual turnover',
                                                               'B': '€10 million or 2% of global annual turnover',
                                                               'C': '€20 million or 4% of global annual turnover',
                                                               'D': '€50 million or 10% of global annual turnover'},
                                                'question': 'What is the maximum fine under GDPR for the most serious '
                                                            'violations?',
                                                'wrong_explanations': {   'A': '€1M / 1% applies to minor violations '
                                                                               'in some jurisdictions — not the GDPR '
                                                                               'maximum.',
                                                                          'B': '€10M / 2% is the lower tier of GDPR '
                                                                               'fines for less serious infringements.',
                                                                          'D': '€50M / 10% is not the GDPR fine '
                                                                               'structure.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Guidelines are optional recommendations (flexible), '
                                                               'while Procedures are mandatory step-by-step '
                                                               'instructions that explain how to implement specific '
                                                               'policies/standards.',
                                                'options': {   'A': 'Guidelines are mandatory; procedures are optional '
                                                                    '— this is backwards — guidelines are optional, '
                                                                    'not mandatory',
                                                               'B': 'Guidelines are flexible recommendations; '
                                                                    'procedures are step-by-step instructions for '
                                                                    'implementing standards',
                                                               'C': 'Guidelines apply to all users; procedures apply '
                                                                    'only to IT staff — applicability is defined per '
                                                                    'policy, not by the type',
                                                               'D': 'They are synonymous terms — they are distinct '
                                                                    'levels in the policy hierarchy'},
                                                'question': "What is the difference between 'Guidelines' and "
                                                            "'Procedures' in the IT Security Policy Framework?",
                                                'wrong_explanations': {   'A': 'This is backwards — guidelines are '
                                                                               'optional, not mandatory.',
                                                                          'C': 'Applicability is defined per policy, '
                                                                               'not by the type.',
                                                                          'D': 'They are distinct levels in the policy '
                                                                               'hierarchy.'}},
                                            {   'correct': 'A',
                                                'explanation': 'GDPR Article 6 lawful bases: (1) Consent, (2) '
                                                               'Contract, (3) Legal Obligation, (4) Vital Interests, '
                                                               '(5) Public Task, (6) Legitimate Interests. At least '
                                                               'one must apply for lawful processing.',
                                                'options': {   'A': 'Consent, Contract, Legal Obligation, Vital '
                                                                    'Interests, Public Task, Legitimate Interests',
                                                               'B': 'Consent, Permission, Contract, Emergency, Public, '
                                                                    "Business — 'Permission' and 'Emergency' are not "
                                                                    'GDPR lawful bases',
                                                               'C': 'Consent, Contract, GDPR Mandate, National '
                                                                    'Security, Public Benefit, Commercial Need',
                                                               'D': 'Explicit Consent, Implicit Consent, Business '
                                                                    'Need, Legal, Medical, Government'},
                                                'question': 'Under GDPR, what are the six lawful bases for processing '
                                                            'personal data?',
                                                'wrong_explanations': {   'B': "'Permission' and 'Emergency' are not "
                                                                               'GDPR lawful bases.',
                                                                          'C': 'GDPR Mandate and Commercial Need are '
                                                                               'not listed bases.',
                                                                          'D': "'Implicit Consent' is not a recognised "
                                                                               'GDPR basis — consent must be freely '
                                                                               'given, specific, informed, and '
                                                                               'unambiguous.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Privacy by Design (GDPR Article 25) requires data '
                                                               'protection to be considered at the design stage — '
                                                               'building privacy in from the beginning rather than '
                                                               'retrofitting it. Includes data minimisation and '
                                                               'pseudonymisation.',
                                                'options': {   'A': 'Designing private office spaces for data '
                                                                    'protection officers — office design is not '
                                                                    'Privacy by Design',
                                                               'B': 'Embedding privacy protections into systems and '
                                                                    'processes from the start of design, rather than '
                                                                    'adding them as an afterthought',
                                                               'C': 'A GDPR requirement to use privacy-preserving '
                                                                    'software only — privacy by Design is a principle, '
                                                                    'not a requirement to use specific software',
                                                               'D': 'Designing websites without cookies — avoiding '
                                                                    'cookies is one small example — Privacy by Design '
                                                                    'is a comprehensive approach'},
                                                'question': "What is 'Privacy by Design'?",
                                                'wrong_explanations': {   'A': 'Office design is not Privacy by '
                                                                               'Design.',
                                                                          'C': 'Privacy by Design is a principle, not '
                                                                               'a requirement to use specific '
                                                                               'software.',
                                                                          'D': 'Avoiding cookies is one small example '
                                                                               '— Privacy by Design is a comprehensive '
                                                                               'approach.'}},
                                            {   'correct': 'A',
                                                'explanation': 'CMA 1990 Section 1: Unauthorised access to computer '
                                                               "material — the basic 'hacking' offence. Maximum "
                                                               "sentence: 2 years imprisonment. You don't need to "
                                                               'succeed in accessing data — the attempt is sufficient.',
                                                'options': {   'A': 'Unauthorised access to computer material',
                                                               'B': 'Unauthorised access with intent to commit further '
                                                                    'offences',
                                                               'C': 'Unauthorised modification of computer material',
                                                               'D': 'Making, supplying, or obtaining articles for '
                                                                    'computer misuse'},
                                                'question': 'Under the Computer Misuse Act 1990, what is a Section 1 '
                                                            'offence?',
                                                'wrong_explanations': {   'B': 'Unauthorised access WITH intent to '
                                                                               'commit further crimes is Section 2 — '
                                                                               'more serious.',
                                                                          'C': 'Unauthorised modification (deleting '
                                                                               'files, installing malware) is Section '
                                                                               '3.',
                                                                          'D': 'Making/supplying/obtaining hacking '
                                                                               'tools is Section 3A (added by Police & '
                                                                               'Justice Act 2006).'}},
                                            {   'correct': 'B',
                                                'explanation': 'Under GDPR Article 15, individuals have the right to '
                                                               'request a copy of their personal data from any '
                                                               'organisation holding it. Organisations must respond '
                                                               'within one month, usually for free.',
                                                'options': {   'A': "A hacker's request to access a company's database "
                                                                    "— a hacker's unauthorised data access is a "
                                                                    'breach, not a DSAR',
                                                               'B': 'A formal request by an individual to obtain a '
                                                                    'copy of their personal data held by an '
                                                                    'organisation',
                                                               'C': "A regulator's request to audit a company's data "
                                                                    "practices — a regulator's audit is a supervisory "
                                                                    'authority investigation — separate from DSAR',
                                                               'D': 'A request to delete all personal data held about '
                                                                    'an individual — requesting deletion is the Right '
                                                                    'to Erasure (Article 17) — separate from a DSAR'},
                                                'question': "What is a 'Data Subject Access Request' (DSAR)?",
                                                'wrong_explanations': {   'A': "A hacker's unauthorised data access is "
                                                                               'a breach, not a DSAR.',
                                                                          'C': "A regulator's audit is a supervisory "
                                                                               'authority investigation — separate '
                                                                               'from DSAR.',
                                                                          'D': 'Requesting deletion is the Right to '
                                                                               'Erasure (Article 17) — separate from a '
                                                                               'DSAR.'}},
                                            {   'correct': 'B',
                                                'explanation': 'GDPR Article 33 requires notifying the supervisory '
                                                               'authority (ICO in the UK) within 72 hours of becoming '
                                                               'aware of a personal data breach, unless it is unlikely '
                                                               'to result in a risk to individuals.',
                                                'options': {   'A': 'Within 24 hours of discovery — 24 hours is not '
                                                                    "the GDPR timeframe — it's 72 hours",
                                                               'B': 'Within 72 hours of becoming aware of the breach '
                                                                    '(where feasible)',
                                                               'C': 'Within 7 days of discovery — 7 days is too long — '
                                                                    'GDPR requires 72 hours',
                                                               'D': 'Only if more than 1000 individuals are affected — '
                                                                    'there is no minimum number of individuals '
                                                                    'affected — the risk to individuals determines '
                                                                    'notification'},
                                                'question': 'What is the GDPR requirement for reporting a personal '
                                                            'data breach to the supervisory authority?',
                                                'wrong_explanations': {   'A': '24 hours is not the GDPR timeframe — '
                                                                               "it's 72 hours.",
                                                                          'C': '7 days is too long — GDPR requires 72 '
                                                                               'hours.',
                                                                          'D': 'There is no minimum number of '
                                                                               'individuals affected — the risk to '
                                                                               'individuals determines notification.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Data minimisation (GDPR Article 5(1)(c)) means '
                                                               'collecting only what is adequate, relevant, and '
                                                               'limited to what is necessary. Organisations should not '
                                                               "collect data 'just in case' it might be useful.",
                                                'options': {   'A': 'Storing data in compressed formats to save space '
                                                                    '— compressed storage is a technical '
                                                                    'implementation — not data minimisation',
                                                               'B': 'Collecting and processing only the minimum '
                                                                    'personal data necessary for the specific purpose',
                                                               'C': 'Deleting all data after one year — data retention '
                                                                    'periods are set by purpose — not a fixed one-year '
                                                                    'rule',
                                                               'D': 'Minimising the number of staff with data access — '
                                                                    'limiting staff access is the principle of least '
                                                                    'privilege — not data minimisation'},
                                                'question': "What does 'data minimisation' mean under GDPR?",
                                                'wrong_explanations': {   'A': 'Compressed storage is a technical '
                                                                               'implementation — not data '
                                                                               'minimisation.',
                                                                          'C': 'Data retention periods are set by '
                                                                               'purpose — not a fixed one-year rule.',
                                                                          'D': 'Limiting staff access is the principle '
                                                                               'of least privilege — not data '
                                                                               'minimisation.'}},
                                            {   'correct': 'B',
                                                'explanation': "The ICO is the UK's supervisory authority for data "
                                                               'protection — it investigates complaints, audits '
                                                               'organisations, issues guidance, and can impose fines '
                                                               'up to £17.5 million or 4% of global turnover.',
                                                'options': {   'A': 'A UK government department that writes data '
                                                                    'protection laws — laws are made by Parliament — '
                                                                    'the ICO enforces them',
                                                               'B': "The UK's independent authority upholding "
                                                                    'information rights — the supervisory authority '
                                                                    'for GDPR/DPA 2018 enforcement',
                                                               'C': 'An international committee that sets GDPR policy '
                                                                    "— gDPR is EU law — the ICO enforces the UK's "
                                                                    'equivalent (UK GDPR / DPA 2018) post-Brexit',
                                                               'D': 'A cybersecurity certification body — the ICO is a '
                                                                    'regulatory authority, not a certification body'},
                                                'question': "What is the ICO (Information Commissioner's Office)?",
                                                'wrong_explanations': {   'A': 'Laws are made by Parliament — the ICO '
                                                                               'enforces them.',
                                                                          'C': 'GDPR is EU law — the ICO enforces the '
                                                                               "UK's equivalent (UK GDPR / DPA 2018) "
                                                                               'post-Brexit.',
                                                                          'D': 'The ICO is a regulatory authority, not '
                                                                               'a certification body.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Purpose limitation (Article 5(1)(b)) means you must '
                                                               'state your purpose for collecting data upfront, and '
                                                               'cannot use it for something different without separate '
                                                               'justification.',
                                                'options': {   'A': 'Limiting the amount of data stored — limiting '
                                                                    'data amounts is data minimisation (Article '
                                                                    '5(1)(c))',
                                                               'B': 'Personal data must only be collected for '
                                                                    'specified, explicit, and legitimate purposes — '
                                                                    'and not further processed in ways incompatible '
                                                                    'with those purposes',
                                                               'C': 'Limiting who can access personal data — limiting '
                                                                    'access is the principle of least privilege',
                                                               'D': 'Restricting data transfers to the EU only — '
                                                                    'restricting data transfers relates to Chapter V '
                                                                    'GDPR transfer rules'},
                                                'question': "What is 'purpose limitation' under GDPR?",
                                                'wrong_explanations': {   'A': 'Limiting data amounts is data '
                                                                               'minimisation (Article 5(1)(c)).',
                                                                          'C': 'Limiting access is the principle of '
                                                                               'least privilege.',
                                                                          'D': 'Restricting data transfers relates to '
                                                                               'Chapter V GDPR transfer rules.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Pseudonymisation replaces directly identifying '
                                                               'information with a pseudonym — the link between '
                                                               'pseudonym and real identity is held separately with '
                                                               'access controls. It reduces risk but data can still be '
                                                               're-identified (unlike anonymisation).',
                                                'options': {   'A': 'Using a fake name when collecting data — using a '
                                                                    'fake name when collecting data is fraud, not '
                                                                    'pseudonymisation',
                                                               'B': 'Processing personal data so it can no longer be '
                                                                    'attributed to a specific individual without '
                                                                    'additional information held separately',
                                                               'C': 'Deleting identifying information from a dataset '
                                                                    'permanently — permanently removing all '
                                                                    'identifiers is anonymisation — pseudonymised data '
                                                                    'can still be re-linked',
                                                               'D': 'Encrypting personal data with AES-256 — '
                                                                    'encryption is a security measure — '
                                                                    'pseudonymisation specifically replaces '
                                                                    'identifiers with pseudonyms'},
                                                'question': "What is 'pseudonymisation' under GDPR?",
                                                'wrong_explanations': {   'A': 'Using a fake name when collecting data '
                                                                               'is fraud, not pseudonymisation.',
                                                                          'C': 'Permanently removing all identifiers '
                                                                               'is anonymisation — pseudonymised data '
                                                                               'can still be re-linked.',
                                                                          'D': 'Encryption is a security measure — '
                                                                               'pseudonymisation specifically replaces '
                                                                               'identifiers with pseudonyms.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Section 3A (added by the Police & Justice Act 2006) '
                                                               'criminalises creating, distributing, or possessing '
                                                               'tools intended for computer misuse — e.g., malware, '
                                                               'exploitation frameworks used with criminal intent.',
                                                'options': {   'A': 'Unauthorised access to any computer — '
                                                                    'unauthorised access is Section 1',
                                                               'B': 'Making, supplying, or obtaining tools or articles '
                                                                    'for use in computer misuse offences',
                                                               'C': 'Causing serious damage to national security '
                                                                    'systems — causing serious damage to national '
                                                                    'security is under Section 3ZA (added by Serious '
                                                                    'Crime Act 2015)',
                                                               'D': 'Unauthorised modification of computer material — '
                                                                    'unauthorised modification is Section 3'},
                                                'question': 'Under the Computer Misuse Act, what is a Section 3A '
                                                            'offence?',
                                                'wrong_explanations': {   'A': 'Unauthorised access is Section 1.',
                                                                          'C': 'Causing serious damage to national '
                                                                               'security is under Section 3ZA (added '
                                                                               'by Serious Crime Act 2015).',
                                                                          'D': 'Unauthorised modification is Section '
                                                                               '3.'}},
                                            {   'correct': 'B',
                                                'explanation': 'GDPR Article 20 gives individuals the right to receive '
                                                               'their personal data in a structured, commonly used, '
                                                               'machine-readable format (e.g., JSON, CSV) and transfer '
                                                               'it to another controller — e.g., switching banks.',
                                                'options': {   'A': 'The right to carry physical copies of your data — '
                                                                    'data portability is a digital right — physical '
                                                                    'copies are a separate DSAR right',
                                                               'B': 'The right to receive your personal data in a '
                                                                    'structured, machine-readable format and transfer '
                                                                    'it to another organisation',
                                                               'C': 'The right for organisations to transfer data '
                                                                    'internationally — international data transfers '
                                                                    'are covered by Chapter V GDPR',
                                                               'D': 'The right to port your phone number between '
                                                                    'networks — phone number porting is a telecoms '
                                                                    'regulatory right, not a GDPR concept'},
                                                'question': "What is 'data portability' under GDPR?",
                                                'wrong_explanations': {   'A': 'Data portability is a digital right — '
                                                                               'physical copies are a separate DSAR '
                                                                               'right.',
                                                                          'C': 'International data transfers are '
                                                                               'covered by Chapter V GDPR.',
                                                                          'D': 'Phone number porting is a telecoms '
                                                                               'regulatory right, not a GDPR '
                                                                               'concept.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Article 21 gives individuals the right to object to '
                                                               'processing based on legitimate interests or public '
                                                               'task — the organisation must stop unless it has '
                                                               'compelling legitimate grounds. Direct marketing '
                                                               'objections are absolute.',
                                                'options': {   'A': 'The right to object to any data processing — the '
                                                                    'right to object is not absolute for all '
                                                                    'processing bases — it applies to specific bases',
                                                               'B': 'The right to object to processing based on '
                                                                    'legitimate interests or for direct marketing '
                                                                    'purposes',
                                                               'C': 'The right to object to being profiled by '
                                                                    'algorithms — profiling objections are related but '
                                                                    'covered more specifically in Article 22',
                                                               'D': 'The right for organisations to object to data '
                                                                    'subject requests — gDPR rights belong to data '
                                                                    'subjects — organisations cannot object to lawful '
                                                                    'requests'},
                                                'question': "What is the 'right to object' under GDPR (Article 21)?",
                                                'wrong_explanations': {   'A': 'The right to object is not absolute '
                                                                               'for all processing bases — it applies '
                                                                               'to specific bases.',
                                                                          'C': 'Profiling objections are related but '
                                                                               'covered more specifically in Article '
                                                                               '22.',
                                                                          'D': 'GDPR rights belong to data subjects — '
                                                                               'organisations cannot object to lawful '
                                                                               'requests.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Legitimate Interests (Article 6(1)(f)) requires a '
                                                               'three-part test: (1) legitimate purpose, (2) '
                                                               "necessary, (3) individual's rights and interests don't "
                                                               "override the controller's interests. It's flexible but "
                                                               'requires documentation.',
                                                'options': {   'A': 'Any legitimate business reason for processing '
                                                                    "data — 'Any legitimate business reason' is too "
                                                                    'broad — a balancing test is required',
                                                               'B': 'A lawful basis allowing processing where the '
                                                                    "controller's (or third party's) interests "
                                                                    "override the individual's rights — requires a "
                                                                    'balancing test',
                                                               'C': 'Interests deemed legitimate by the ICO — the ICO '
                                                                    'does not pre-approve legitimate interests — '
                                                                    'organisations self-assess',
                                                               'D': 'Processing for the purpose of preventing '
                                                                    'cybercrime — processing for cybercrime prevention '
                                                                    'could use this basis but must still pass the '
                                                                    'balancing test'},
                                                'question': "What is 'legitimate interests' as a lawful basis for "
                                                            'processing under GDPR?',
                                                'wrong_explanations': {   'A': "'Any legitimate business reason' is "
                                                                               'too broad — a balancing test is '
                                                                               'required.',
                                                                          'C': 'The ICO does not pre-approve '
                                                                               'legitimate interests — organisations '
                                                                               'self-assess.',
                                                                          'D': 'Processing for cybercrime prevention '
                                                                               'could use this basis but must still '
                                                                               'pass the balancing test.'}},
                                            {   'correct': 'B',
                                                'explanation': 'GDPR Articles 13/14 require providing a privacy notice '
                                                               '(privacy policy) when collecting personal data — '
                                                               'covering: identity of controller, purpose, legal '
                                                               'basis, retention period, and data subject rights.',
                                                'options': {   'A': 'Send an email confirmation — email confirmation '
                                                                    'is not required by GDPR as the privacy notice '
                                                                    'mechanism',
                                                               'B': 'Provide a privacy notice at the point of '
                                                                    'collection — explaining who collects the data, '
                                                                    "why, how long it's kept, and individuals' rights",
                                                               'C': 'Obtain written consent regardless of lawful basis '
                                                                    '— consent is only one of six lawful bases — not '
                                                                    'required for all processing',
                                                               'D': 'Register the data collection with the ICO first — '
                                                                    'iCO registration (GDPR Article 30) is about '
                                                                    'maintaining records, not pre-approval of data '
                                                                    'collection'},
                                                'question': 'What must organisations do when collecting personal data '
                                                            'from individuals under GDPR?',
                                                'wrong_explanations': {   'A': 'Email confirmation is not required by '
                                                                               'GDPR as the privacy notice mechanism.',
                                                                          'C': 'Consent is only one of six lawful '
                                                                               'bases — not required for all '
                                                                               'processing.',
                                                                          'D': 'ICO registration (GDPR Article 30) is '
                                                                               'about maintaining records, not '
                                                                               'pre-approval of data collection.'}},
                                            {   'correct': 'B',
                                                'explanation': 'AUPs set out what employees can and cannot do with IT '
                                                               'assets — preventing misuse, protecting the '
                                                               'organisation from legal liability, and setting clear '
                                                               'expectations about acceptable behaviour.',
                                                'options': {   'A': 'Technical vulnerabilities in IT systems — '
                                                                    'technical vulnerabilities are addressed by '
                                                                    'security controls, not AUPs directly',
                                                               'B': 'Misuse of IT assets — protecting against '
                                                                    'activities like using work computers for illegal '
                                                                    'downloads, accessing inappropriate content, or '
                                                                    'transmitting confidential data insecurely',
                                                               'C': 'Physical theft of IT equipment — physical '
                                                                    'security is handled by physical security policies',
                                                               'D': 'Data breaches caused by hackers — hacker attacks '
                                                                    'are addressed by technical security — AUPs govern '
                                                                    'user behaviour'},
                                                'question': "What is an 'Acceptable Use Policy' (AUP) designed to "
                                                            'prevent?',
                                                'wrong_explanations': {   'A': 'Technical vulnerabilities are '
                                                                               'addressed by security controls, not '
                                                                               'AUPs directly.',
                                                                          'C': 'Physical security is handled by '
                                                                               'physical security policies.',
                                                                          'D': 'Hacker attacks are addressed by '
                                                                               'technical security — AUPs govern user '
                                                                               'behaviour.'}},
                                            {   'correct': 'B',
                                                'explanation': 'GDPR consent must be: freely given (no coercion), '
                                                               'specific (per purpose), informed (person knows what '
                                                               "they're agreeing to), and unambiguous (clear "
                                                               'affirmative action — pre-ticked boxes are invalid).',
                                                'options': {   'A': 'Any agreement to terms and conditions — agreeing '
                                                                    'to T&Cs is not automatically valid GDPR consent — '
                                                                    'the conditions must be met',
                                                               'B': 'Freely given, specific, informed, and unambiguous '
                                                                    "indication of the data subject's wishes — must be "
                                                                    'as easy to withdraw as to give',
                                                               'C': 'Assumed consent when someone provides their email '
                                                                    'address — assumed/implied consent is not valid '
                                                                    'GDPR consent — it must be an affirmative action',
                                                               'D': 'Parental consent for processing any data — '
                                                                    'consent applies to all data subjects — parental '
                                                                    'consent is specifically required for children '
                                                                    'under 13-16 (varies by member state)'},
                                                'question': "What is 'consent' as a lawful basis for GDPR processing?",
                                                'wrong_explanations': {   'A': 'Agreeing to T&Cs is not automatically '
                                                                               'valid GDPR consent — the conditions '
                                                                               'must be met.',
                                                                          'C': 'Assumed/implied consent is not valid '
                                                                               'GDPR consent — it must be an '
                                                                               'affirmative action.',
                                                                          'D': 'Consent applies to all data subjects — '
                                                                               'parental consent is specifically '
                                                                               'required for children under 13-16 '
                                                                               '(varies by member state).'}},
                                            {   'correct': 'B',
                                                'explanation': 'The key difference is authorisation. Ethical hackers '
                                                               'have written permission (scope, rules of engagement) '
                                                               'from the organisation — they use the same techniques '
                                                               'as attackers but legally and to improve security.',
                                                'options': {   'A': 'Ethical hacking uses different tools than '
                                                                    'malicious hacking — ethical and malicious hackers '
                                                                    'often use the same tools — the difference is '
                                                                    'authorisation',
                                                               'B': 'Ethical hacking is performed with explicit '
                                                                    'written authorisation from the system owner — '
                                                                    'malicious hacking is unauthorised',
                                                               'C': 'Ethical hacking only tests public-facing systems '
                                                                    '— authorised testing can include internal '
                                                                    'systems, not just public-facing ones',
                                                               'D': 'Ethical hacking does not exploit vulnerabilities '
                                                                    '— ethical hackers do exploit vulnerabilities — '
                                                                    'under controlled, authorised conditions'},
                                                'question': "What is 'ethical hacking' and how is it different from "
                                                            'malicious hacking?',
                                                'wrong_explanations': {   'A': 'Ethical and malicious hackers often '
                                                                               'use the same tools — the difference is '
                                                                               'authorisation.',
                                                                          'C': 'Authorised testing can include '
                                                                               'internal systems, not just '
                                                                               'public-facing ones.',
                                                                          'D': 'Ethical hackers do exploit '
                                                                               'vulnerabilities — under controlled, '
                                                                               'authorised conditions.'}},
                                            {   'correct': 'B',
                                                'explanation': 'Cyber insurance covers costs arising from cyber '
                                                               'incidents: incident response, legal costs, regulatory '
                                                               'fines, customer notification, PR, business '
                                                               'interruption, and sometimes ransomware payments.',
                                                'options': {   'A': 'Insurance for IT equipment against physical '
                                                                    'damage — physical equipment damage is covered by '
                                                                    'standard property insurance',
                                                               'B': 'Insurance that covers financial losses from cyber '
                                                                    'incidents — breach response costs, legal fees, '
                                                                    'ransom payments, business interruption',
                                                               'C': 'Liability insurance for cybersecurity companies — '
                                                                    'professional liability for cybersecurity firms is '
                                                                    'a different product',
                                                               'D': 'Government-funded compensation for cybercrime '
                                                                    'victims — government compensation schemes for '
                                                                    'cybercrime are separate from commercial cyber '
                                                                    'insurance'},
                                                'question': "What is 'cybersecurity insurance' and what does it cover?",
                                                'wrong_explanations': {   'A': 'Physical equipment damage is covered '
                                                                               'by standard property insurance.',
                                                                          'C': 'Professional liability for '
                                                                               'cybersecurity firms is a different '
                                                                               'product.',
                                                                          'D': 'Government compensation schemes for '
                                                                               'cybercrime are separate from '
                                                                               'commercial cyber insurance.'}},
                                            {   'correct': 'B',
                                                'explanation': 'PECR (2003) sits alongside UK GDPR and covers: '
                                                               'email/SMS/phone marketing rules, cookie consent '
                                                               'requirements, and confidentiality of electronic '
                                                               'communications. Enforced by the ICO.',
                                                'options': {   'A': 'Physical privacy in electronic surveillance — '
                                                                    'surveillance is covered by the Investigatory '
                                                                    'Powers Act — not PECR',
                                                               'B': 'Rules on electronic marketing, cookies, and '
                                                                    'confidentiality of electronic communications',
                                                               'C': 'Criminal offences related to electronic fraud — '
                                                                    'electronic fraud offences are under the Fraud Act '
                                                                    '2006',
                                                               'D': 'Data protection in electronic health records — '
                                                                    'health data protection is covered by UK GDPR with '
                                                                    'additional controls — not primarily PECR'},
                                                'question': 'What does the PECR (Privacy and Electronic Communications '
                                                            'Regulations) cover in the UK?',
                                                'wrong_explanations': {   'A': 'Surveillance is covered by the '
                                                                               'Investigatory Powers Act — not PECR.',
                                                                          'C': 'Electronic fraud offences are under '
                                                                               'the Fraud Act 2006.',
                                                                          'D': 'Health data protection is covered by '
                                                                               'UK GDPR with additional controls — not '
                                                                               'primarily PECR.'}}],
    'Week 3 - CIA Triad & Cryptography': [   {   'correct': 'B',
                                                 'explanation': 'CIA = Confidentiality (keeping data secret), '
                                                                'Integrity (ensuring data is accurate/untampered), '
                                                                'Availability (ensuring systems/data are accessible '
                                                                'when needed).',
                                                 'options': {   'A': 'Cybersecurity, Intelligence, Authorisation',
                                                                'B': 'Confidentiality, Integrity, Availability',
                                                                'C': 'Control, Integrity, Authentication',
                                                                'D': 'Confidentiality, Identification, Access'},
                                                 'question': 'What does the CIA Triad stand for?',
                                                 'wrong_explanations': {   'A': 'Incorrect — CIA Triad is a '
                                                                                'foundational security model.',
                                                                           'C': 'Incorrect terms — Control and '
                                                                                'Authentication are not part of the '
                                                                                'CIA Triad.',
                                                                           'D': 'Identification and Access are part of '
                                                                                'access control models, not the CIA '
                                                                                'Triad.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'Deterministic means the same input always produces '
                                                                'the same hash. This is essential for password '
                                                                'verification — compare hashes rather than plaintext.',
                                                 'options': {   'A': 'Collision resistance',
                                                                'B': 'One-way property',
                                                                'C': 'Deterministic',
                                                                'D': 'Avalanche effect'},
                                                 'question': 'Which property of a cryptographic hash function means '
                                                             'the same input ALWAYS produces the same output?',
                                                 'wrong_explanations': {   'A': "Collision resistance means it's "
                                                                                'computationally infeasible to find '
                                                                                'two inputs with the same hash.',
                                                                           'B': 'One-way means you cannot reverse a '
                                                                                'hash to recover the original input.',
                                                                           'D': 'Avalanche effect means a tiny change '
                                                                                'in input causes a completely '
                                                                                'different output hash.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'Hashing provides confidentiality. A compromised '
                                                                'database only yields hashes. Since hashing is '
                                                                'one-way, reversing it is computationally impractical.',
                                                 'options': {   'A': 'Hashes are smaller and save storage — storage '
                                                                     'efficiency is not the main reason',
                                                                'B': 'Hashes can be decrypted by admins if needed — '
                                                                     'hashes are ONE-WAY — they cannot be decrypted '
                                                                     'like encryption',
                                                                'C': 'If the database is compromised, the attacker '
                                                                     'must reverse the hash to find the password',
                                                                'D': 'Hashing automatically meets GDPR requirements — '
                                                                     "gDPR requires 'appropriate security measures' "
                                                                     "but doesn't specifically mandate hashing"},
                                                 'question': 'Why are passwords stored as hashes rather than '
                                                             'plaintext?',
                                                 'wrong_explanations': {   'A': 'Storage efficiency is not the main '
                                                                                'reason.',
                                                                           'B': 'Hashes are ONE-WAY — they cannot be '
                                                                                'decrypted like encryption.',
                                                                           'D': "GDPR requires 'appropriate security "
                                                                                "measures' but doesn't specifically "
                                                                                'mandate hashing.'}},
                                             {   'correct': 'B',
                                                 'explanation': "The MD5 hash of 'cat' is "
                                                                'd077f244def8a70e5ea758bd8352fcd8. This is shown in '
                                                                'the lecture to demonstrate the avalanche effect — '
                                                                "notice how 'cats' produces a completely different "
                                                                'hash.',
                                                 'options': {   'A': '5c4bf758b3e4a924c49c4cd683cc638b',
                                                                'B': 'd077f244def8a70e5ea758bd8352fcd8',
                                                                'C': '0832c1202da8d382318e329a7c133ea0',
                                                                'D': '66f4002e64af1f1b1ac2ec01d3e79635'},
                                                 'question': "What is the MD5 hash of the word 'cat'?",
                                                 'wrong_explanations': {   'A': '5c4bf758b3e4a924c49c4cd683cc638b is '
                                                                                'from the account credentials example.',
                                                                           'C': '0832c1202da8d382318e329a7c133ea0 is '
                                                                                "the MD5 hash of 'cats'.",
                                                                           'D': '66f4002e64af1f1b1ac2ec01d3e79635 is '
                                                                                'the MD5 hash of the long poem.'}},
                                             {   'correct': 'A',
                                                 'explanation': 'MD5 always produces a 128-bit (16-byte, 32 hex '
                                                                'character) output regardless of the input size.',
                                                 'options': {   'A': '16 bytes = 32 hex = 128 bits',
                                                                'B': '32 bytes = 64 hex = 256 bits',
                                                                'C': '8 bytes = 16 hex = 64 bits',
                                                                'D': '64 bytes = 128 hex = 512 bits'},
                                                 'question': 'What is the output size of an MD5 hash?',
                                                 'wrong_explanations': {   'B': '32 bytes / 256 bits describes '
                                                                                'SHA-256.',
                                                                           'C': '64-bit hashes are not a standard '
                                                                                'algorithm size.',
                                                                           'D': '64 bytes / 512 bits describes '
                                                                                'SHA-512.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The avalanche effect means even a tiny change (e.g., '
                                                                "'cat' vs 'cats') produces a hash that appears "
                                                                'completely random and different — as demonstrated in '
                                                                'the lecture.',
                                                 'options': {   'A': 'Large inputs take longer to hash — that is about '
                                                                     'performance, not the avalanche effect',
                                                                'B': 'A small change in the input produces a '
                                                                     'completely different hash output',
                                                                'C': 'The same input always produces the same hash — '
                                                                     'that describes the deterministic property',
                                                                'D': 'Hash functions can be reversed given enough '
                                                                     'computing power'},
                                                 'question': "What does the 'avalanche effect' mean in cryptographic "
                                                             'hash functions?',
                                                 'wrong_explanations': {   'A': 'That is about performance, not the '
                                                                                'avalanche effect.',
                                                                           'C': 'That describes the deterministic '
                                                                                'property.',
                                                                           'D': 'That contradicts the one-way property '
                                                                                'of hash functions.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'Encrypting network traffic is done by protocols like '
                                                                'TLS/SSL, not hash functions. Hash functions are used '
                                                                'for: protecting passwords, validating integrity, '
                                                                'blockchain, and digital signatures.',
                                                 'options': {   'A': 'Protecting passwords',
                                                                'B': 'Validating data integrity',
                                                                'C': 'Encrypting network traffic',
                                                                'D': 'Blockchain and digital signatures'},
                                                 'question': 'Which of the following is NOT a use case for '
                                                             'cryptographic hash functions mentioned in the lecture?',
                                                 'wrong_explanations': {   'A': 'Protecting passwords is explicitly '
                                                                                'listed as a use case.',
                                                                           'B': 'Validating integrity (detecting '
                                                                                'modifications) is explicitly listed.',
                                                                           'D': 'Blockchain and digital signatures are '
                                                                                'explicitly listed.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'SHA-256 produces a 256-bit (32-byte, 64 hex '
                                                                'character) output. This is shown in the lecture '
                                                                'alongside the 128-bit MD5 example.',
                                                 'options': {   'A': 'MD5',
                                                                'B': 'SHA-1',
                                                                'C': 'SHA-256',
                                                                'D': 'RipeMD128'},
                                                 'question': 'Which hash algorithm produces a 256-bit output (32 bytes '
                                                             '= 64 hex values)?',
                                                 'wrong_explanations': {   'A': 'MD5 produces 128 bits / 32 hex '
                                                                                'characters.',
                                                                           'B': 'SHA-1 produces 160 bits / 40 hex '
                                                                                'characters.',
                                                                           'D': 'RipeMD128 produces 128 bits.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'Confidentiality means ensuring data is only '
                                                                'accessible to authorised parties. It protects against '
                                                                'unauthorised disclosure of information.',
                                                 'options': {   'A': 'Ensuring data cannot be modified by unauthorised '
                                                                     'users',
                                                                'B': 'Ensuring systems are accessible when needed',
                                                                'C': 'Ensuring data is only accessible to authorised '
                                                                     'parties',
                                                                'D': 'Ensuring all user actions are logged — logging '
                                                                     'is part of accountability/auditing, not '
                                                                     'Confidentiality'},
                                                 'question': "What does 'Confidentiality' mean in the CIA Triad?",
                                                 'wrong_explanations': {   'A': 'That describes Integrity.',
                                                                           'B': 'That describes Availability.',
                                                                           'D': 'Logging is part of '
                                                                                'accountability/auditing, not '
                                                                                'Confidentiality.'}},
                                             {   'correct': 'B',
                                                 'explanation': "Adding just one letter 's' produces a completely "
                                                                'different hash. This is the avalanche effect — a '
                                                                'small input change causes a drastically different '
                                                                'output, making it hard to predict patterns.',
                                                 'options': {   'A': 'MD5 is broken and produces similar hashes for '
                                                                     'similar inputs',
                                                                'B': 'The avalanche effect — a tiny change produces a '
                                                                     'completely different hash',
                                                                'C': 'MD5 is reversible from short inputs — mD5 is a '
                                                                     'one-way function and is not reversible',
                                                                'D': 'SHA-256 would produce the same hashes for both — '
                                                                     'sHA-256 would also produce completely different '
                                                                     "hashes for 'cat' and 'cats'"},
                                                 'question': "The MD5 hash of 'cats' is "
                                                             "0832c1202da8d382318e329a7c133ea0. The hash of 'cat' is "
                                                             'd077f244def8a70e5ea758bd8352fcd8. What does this '
                                                             'demonstrate?',
                                                 'wrong_explanations': {   'A': 'MD5 does NOT produce similar hashes — '
                                                                                'the two hashes look completely '
                                                                                'unrelated.',
                                                                           'C': 'MD5 is a one-way function and is not '
                                                                                'reversible.',
                                                                           'D': 'SHA-256 would also produce completely '
                                                                                "different hashes for 'cat' and "
                                                                                "'cats'."}},
                                             {   'correct': 'B',
                                                 'explanation': 'A salt is a random value added to a password before '
                                                                'hashing. This means identical passwords produce '
                                                                'different hashes, defeating pre-computed rainbow '
                                                                'table attacks.',
                                                 'options': {   'A': 'Encrypting the hash with a symmetric key — '
                                                                     'encrypting a hash adds a layer but is not '
                                                                     'salting',
                                                                'B': 'Adding a random value to the password before '
                                                                     'hashing to prevent rainbow table attacks',
                                                                'C': 'Using SHA-256 instead of MD5 — algorithm choice '
                                                                     'is separate from salting — you can salt MD5 or '
                                                                     'SHA-256',
                                                                'D': 'Storing the hash in a separate database — '
                                                                     'separate storage is a security measure but not '
                                                                     'what salting means'},
                                                 'question': "What is 'salting' in the context of password hashing?",
                                                 'wrong_explanations': {   'A': 'Encrypting a hash adds a layer but is '
                                                                                'not salting.',
                                                                           'C': 'Algorithm choice is separate from '
                                                                                'salting — you can salt MD5 or '
                                                                                'SHA-256.',
                                                                           'D': 'Separate storage is a security '
                                                                                'measure but not what salting means.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'MD5 has known collision vulnerabilities — researchers '
                                                                'can craft two different inputs that produce the same '
                                                                'MD5 hash. This makes it unsuitable for digital '
                                                                'signatures and certificates.',
                                                 'options': {   'A': 'MD5 hashes are too long for modern systems — mD5 '
                                                                     'produces a 128-bit hash — length is not the '
                                                                     'issue',
                                                                'B': 'MD5 is vulnerable to collision attacks — two '
                                                                     'different inputs can produce the same hash',
                                                                'C': 'MD5 is too slow for modern processors — mD5 is '
                                                                     'actually very fast — speed can be a '
                                                                     'vulnerability (makes brute-force easier), but '
                                                                     'collision attacks are the main concern',
                                                                'D': 'MD5 does not support Unicode input — input '
                                                                     'encoding is not the reason MD5 is broken'},
                                                 'question': 'Why is MD5 no longer considered cryptographically '
                                                             'secure?',
                                                 'wrong_explanations': {   'A': 'MD5 produces a 128-bit hash — length '
                                                                                'is not the issue.',
                                                                           'C': 'MD5 is actually very fast — speed can '
                                                                                'be a vulnerability (makes brute-force '
                                                                                'easier), but collision attacks are '
                                                                                'the main concern.',
                                                                           'D': 'Input encoding is not the reason MD5 '
                                                                                'is broken.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Integrity means data is accurate and has not been '
                                                                'modified without authorisation. Hash functions are '
                                                                'commonly used to verify integrity — if the hash '
                                                                'changes, the data was altered.',
                                                 'options': {   'A': 'Only authorised people can view the data — that '
                                                                     'describes Confidentiality',
                                                                'B': 'The data is accurate, complete, and has not been '
                                                                     'tampered with',
                                                                'C': 'The data is always accessible when needed — that '
                                                                     'describes Availability',
                                                                'D': 'The data is encrypted at rest — encryption at '
                                                                     'rest supports Confidentiality, not directly '
                                                                     'Integrity'},
                                                 'question': "What does 'Integrity' mean in the CIA Triad?",
                                                 'wrong_explanations': {   'A': 'That describes Confidentiality.',
                                                                           'C': 'That describes Availability.',
                                                                           'D': 'Encryption at rest supports '
                                                                                'Confidentiality, not directly '
                                                                                'Integrity.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'A cryptographic hash (checksum) of the original file '
                                                                'is published. After downloading, you hash the file '
                                                                'and compare — if the hashes match, the file is intact '
                                                                'and unmodified.',
                                                 'options': {   'A': 'Symmetric encryption',
                                                                'B': 'Digital certificate',
                                                                'C': 'Cryptographic hash (checksum)',
                                                                'D': 'VPN tunnel'},
                                                 'question': "Which cryptographic concept allows verifying a file's "
                                                             'integrity after download?',
                                                 'wrong_explanations': {   'A': 'Symmetric encryption provides '
                                                                                'confidentiality, not integrity '
                                                                                'verification by itself.',
                                                                           'B': 'Digital certificates authenticate '
                                                                                'identity but a hash is used for '
                                                                                'simple file integrity checking.',
                                                                           'D': 'A VPN provides secure transmission, '
                                                                                'not file integrity checking.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Symmetric: one shared secret key (fast, used for bulk '
                                                                'data — AES). Asymmetric: public/private key pair '
                                                                '(slower, used for key exchange and digital signatures '
                                                                '— RSA, ECC). TLS uses both.',
                                                 'options': {   'A': 'Symmetric is for data at rest; asymmetric is for '
                                                                     'data in transit — both can be used for data at '
                                                                     'rest or in transit — the distinction is key '
                                                                     'management',
                                                                'B': 'Symmetric uses one shared key for both '
                                                                     'encryption and decryption; asymmetric uses a key '
                                                                     'pair (public key to encrypt, private key to '
                                                                     'decrypt)',
                                                                'C': 'Symmetric is faster but only works for small '
                                                                     'files; asymmetric works for all file sizes — '
                                                                     'symmetric can handle any file size — performance '
                                                                     'is the actual advantage',
                                                                'D': 'Symmetric requires a certificate authority; '
                                                                     'asymmetric does not — both can work with or '
                                                                     'without CAs — asymmetric typically uses PKI but '
                                                                     "doesn't require it"},
                                                 'question': 'What is the difference between symmetric and asymmetric '
                                                             'encryption?',
                                                 'wrong_explanations': {   'A': 'Both can be used for data at rest or '
                                                                                'in transit — the distinction is key '
                                                                                'management.',
                                                                           'C': 'Symmetric can handle any file size — '
                                                                                'performance is the actual advantage.',
                                                                           'D': 'Both can work with or without CAs — '
                                                                                'asymmetric typically uses PKI but '
                                                                                "doesn't require it."}},
                                             {   'correct': 'B',
                                                 'explanation': 'AES is a symmetric block cipher operating on 128-bit '
                                                                'blocks with key sizes of 128, 192, or 256 bits. '
                                                                "Adopted by NIST in 2001, it's used in TLS, disk "
                                                                'encryption (BitLocker), and Wi-Fi (WPA2/WPA3).',
                                                 'options': {   'A': 'An asymmetric encryption algorithm using key '
                                                                     'pairs — key pairs are used by asymmetric '
                                                                     'algorithms like RSA — AES uses a single shared '
                                                                     'key',
                                                                'B': 'A symmetric block cipher that replaced DES, '
                                                                     'supporting 128, 192, or 256-bit keys — the '
                                                                     'current gold standard for symmetric encryption',
                                                                'C': 'A hashing algorithm producing 256-bit outputs — '
                                                                     'sHA-256 produces 256-bit hashes — AES is an '
                                                                     'encryption algorithm',
                                                                'D': 'An algorithm for generating RSA key pairs — rSA '
                                                                     'key generation uses a different algorithm — AES '
                                                                     'is for encryption, not key generation'},
                                                 'question': 'What is AES (Advanced Encryption Standard)?',
                                                 'wrong_explanations': {   'A': 'Key pairs are used by asymmetric '
                                                                                'algorithms like RSA — AES uses a '
                                                                                'single shared key.',
                                                                           'C': 'SHA-256 produces 256-bit hashes — AES '
                                                                                'is an encryption algorithm.',
                                                                           'D': 'RSA key generation uses a different '
                                                                                'algorithm — AES is for encryption, '
                                                                                'not key generation.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'RSA is an asymmetric algorithm where security relies '
                                                                'on the computational difficulty of factoring the '
                                                                'product of two large primes. Key sizes of 2048+ bits '
                                                                'are recommended. Used in TLS, PGP, and digital '
                                                                'signatures.',
                                                 'options': {   'A': 'A symmetric encryption algorithm faster than AES '
                                                                     '— rSA is asymmetric and much slower than AES for '
                                                                     'bulk encryption',
                                                                'B': 'An asymmetric encryption algorithm based on the '
                                                                     'mathematical difficulty of factoring large prime '
                                                                     'numbers',
                                                                'C': 'A hashing algorithm used for password protection '
                                                                     '— rSA is an encryption/signing algorithm, not a '
                                                                     'hashing algorithm',
                                                                'D': 'A network protocol for secure communications — '
                                                                     'rSA is an algorithm, not a protocol — protocols '
                                                                     'like TLS use RSA within them'},
                                                 'question': 'What is RSA (Rivest–Shamir–Adleman)?',
                                                 'wrong_explanations': {   'A': 'RSA is asymmetric and much slower '
                                                                                'than AES for bulk encryption.',
                                                                           'C': 'RSA is an encryption/signing '
                                                                                'algorithm, not a hashing algorithm.',
                                                                           'D': 'RSA is an algorithm, not a protocol — '
                                                                                'protocols like TLS use RSA within '
                                                                                'them.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'A digital signature: sender hashes the data, then '
                                                                'encrypts the hash with their private key. Verifier '
                                                                "decrypts with sender's public key and compares hashes "
                                                                '— proves identity and integrity, and provides '
                                                                'non-repudiation.',
                                                 'options': {   'A': 'An electronic image of a handwritten signature — '
                                                                     'electronic signature images are not '
                                                                     'cryptographic digital signatures — they provide '
                                                                     'no security',
                                                                'B': 'A cryptographic value created by signing data '
                                                                     'with a private key — proves authenticity (who '
                                                                     'signed) and integrity (data was not altered)',
                                                                'C': 'A digital certificate proving server identity — '
                                                                     'digital certificates contain public keys and '
                                                                     'identity information — different from a '
                                                                     'signature on data',
                                                                'D': 'An encrypted message that can only be read by '
                                                                     'the recipient — encrypted messages provide '
                                                                     'confidentiality — digital signatures provide '
                                                                     'authenticity and integrity'},
                                                 'question': 'What is a digital signature and what does it prove?',
                                                 'wrong_explanations': {   'A': 'Electronic signature images are not '
                                                                                'cryptographic digital signatures — '
                                                                                'they provide no security.',
                                                                           'C': 'Digital certificates contain public '
                                                                                'keys and identity information — '
                                                                                'different from a signature on data.',
                                                                           'D': 'Encrypted messages provide '
                                                                                'confidentiality — digital signatures '
                                                                                'provide authenticity and integrity.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'PKI underpins secure internet communication — '
                                                                'Certificate Authorities (CAs) issue digital '
                                                                'certificates that bind a public key to an identity, '
                                                                'enabling trust in HTTPS, email signing, and code '
                                                                'signing.',
                                                 'options': {   'A': 'A private network using public IP addresses — a '
                                                                     'private network using public IPs is a VPN '
                                                                     'concept, not PKI',
                                                                'B': 'A system of hardware, software, policies, and '
                                                                     'procedures for creating, managing, distributing, '
                                                                     'and revoking digital certificates',
                                                                'C': 'An algorithm for generating asymmetric key pairs '
                                                                     '— key generation algorithms (RSA, ECC) are '
                                                                     'components used within PKI, not PKI itself',
                                                                'D': 'A protocol for encrypting public Wi-Fi '
                                                                     'connections — wi-Fi encryption protocols '
                                                                     '(WPA2/3) are separate from PKI'},
                                                 'question': 'What is PKI (Public Key Infrastructure)?',
                                                 'wrong_explanations': {   'A': 'A private network using public IPs is '
                                                                                'a VPN concept, not PKI.',
                                                                           'C': 'Key generation algorithms (RSA, ECC) '
                                                                                'are components used within PKI, not '
                                                                                'PKI itself.',
                                                                           'D': 'Wi-Fi encryption protocols (WPA2/3) '
                                                                                'are separate from PKI.'}},
                                             {   'correct': 'B',
                                                 'explanation': "CAs (e.g., DigiCert, Let's Encrypt) verify identities "
                                                                'and issue X.509 certificates. Your browser trusts '
                                                                'websites because their certificates are signed by a '
                                                                "CA in your browser's trust store.",
                                                 'options': {   'A': 'A government body that authorises encryption '
                                                                     'algorithms — encryption algorithm standards are '
                                                                     'set by bodies like NIST, not CAs',
                                                                'B': 'A trusted entity that issues and signs digital '
                                                                     'certificates, vouching for the identity of the '
                                                                     'certificate holder',
                                                                'C': 'A server that stores private keys for '
                                                                     'organisations — private keys should never leave '
                                                                     'the key owner — CAs do not store private keys',
                                                                'D': 'An organisation that certifies cybersecurity '
                                                                     'professionals — cybersecurity certifications are '
                                                                     'issued by bodies like ISC2, EC-Council — not the '
                                                                     'same as PKI CAs'},
                                                 'question': 'What is a Certificate Authority (CA)?',
                                                 'wrong_explanations': {   'A': 'Encryption algorithm standards are '
                                                                                'set by bodies like NIST, not CAs.',
                                                                           'C': 'Private keys should never leave the '
                                                                                'key owner — CAs do not store private '
                                                                                'keys.',
                                                                           'D': 'Cybersecurity certifications are '
                                                                                'issued by bodies like ISC2, '
                                                                                'EC-Council — not the same as PKI '
                                                                                'CAs.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'TLS (successor to SSL) encrypts data in transit — '
                                                                'HTTPS, SMTPS, IMAPS all use TLS. It provides: '
                                                                'confidentiality (encryption), integrity (HMAC), and '
                                                                'server authentication (certificates).',
                                                 'options': {   'A': 'Encrypting files on a local hard drive — file '
                                                                     'encryption at rest uses tools like BitLocker, '
                                                                     'FileVault — not TLS',
                                                                'B': 'Encrypting communications over a network — '
                                                                     'providing confidentiality, integrity, and '
                                                                     'authentication for protocols like HTTPS',
                                                                'C': 'Authenticating users with two-factor '
                                                                     'authentication — tLS authenticates servers via '
                                                                     'certificates — not users via 2FA',
                                                                'D': 'Filtering malicious network traffic — traffic '
                                                                     'filtering is done by firewalls/IDS — TLS '
                                                                     'provides encryption'},
                                                 'question': 'What is TLS (Transport Layer Security) used for?',
                                                 'wrong_explanations': {   'A': 'File encryption at rest uses tools '
                                                                                'like BitLocker, FileVault — not TLS.',
                                                                           'C': 'TLS authenticates servers via '
                                                                                'certificates — not users via 2FA.',
                                                                           'D': 'Traffic filtering is done by '
                                                                                'firewalls/IDS — TLS provides '
                                                                                'encryption.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Diffie-Hellman allows two parties to independently '
                                                                'compute a shared secret using publicly exchanged '
                                                                'values, without that secret ever being transmitted. '
                                                                "It's the basis of TLS key exchange.",
                                                 'options': {   'A': 'A method for two parties to share passwords '
                                                                     "securely — diffie-Hellman doesn't exchange "
                                                                     'passwords — it establishes a shared '
                                                                     'cryptographic secret',
                                                                'B': 'A mathematical method allowing two parties to '
                                                                     'establish a shared secret key over an insecure '
                                                                     'channel without prior shared secrets',
                                                                'C': 'An asymmetric encryption algorithm for data — '
                                                                     'diffie-Hellman is a key exchange protocol, not '
                                                                     'used for encrypting data directly',
                                                                'D': 'A key derivation function for hashing passwords '
                                                                     '— password hashing uses functions like '
                                                                     'bcrypt/PBKDF2 — not Diffie-Hellman'},
                                                 'question': 'What is the Diffie-Hellman key exchange?',
                                                 'wrong_explanations': {   'A': "Diffie-Hellman doesn't exchange "
                                                                                'passwords — it establishes a shared '
                                                                                'cryptographic secret.',
                                                                           'C': 'Diffie-Hellman is a key exchange '
                                                                                'protocol, not used for encrypting '
                                                                                'data directly.',
                                                                           'D': 'Password hashing uses functions like '
                                                                                'bcrypt/PBKDF2 — not Diffie-Hellman.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'HMAC combines a cryptographic hash (e.g., SHA-256) '
                                                                'with a secret key — producing a value that proves '
                                                                "both that the data hasn't changed (integrity) and "
                                                                'that it came from someone with the key '
                                                                '(authenticity).',
                                                 'options': {   'A': 'A hash function that also encrypts the output — '
                                                                     'hMAC does not encrypt — it authenticates',
                                                                'B': 'A mechanism that combines a hash function with a '
                                                                     'secret key to verify both data integrity and '
                                                                     'authenticity',
                                                                'C': 'A method for generating RSA keys using hashes — '
                                                                     "rSA key generation doesn't use HMAC",
                                                                'D': 'An algorithm for hashing passwords with a salt — '
                                                                     'password hashing with salts uses '
                                                                     'bcrypt/PBKDF2/Argon2 — not HMAC'},
                                                 'question': 'What is HMAC (Hash-based Message Authentication Code)?',
                                                 'wrong_explanations': {   'A': 'HMAC does not encrypt — it '
                                                                                'authenticates.',
                                                                           'C': "RSA key generation doesn't use HMAC.",
                                                                           'D': 'Password hashing with salts uses '
                                                                                'bcrypt/PBKDF2/Argon2 — not HMAC.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Encoding (Base64, URL): converts format, no security '
                                                                '— anyone can reverse it. Encryption: protects data, '
                                                                'requires key to reverse. Hashing: one-way digest, '
                                                                'cannot be reversed, used for integrity/passwords.',
                                                 'options': {   'A': 'They are all the same — different names for the '
                                                                     'same process — they serve fundamentally '
                                                                     'different purposes',
                                                                'B': 'Encoding converts data format (reversible, no '
                                                                     'key); encryption protects confidentiality '
                                                                     '(reversible with key); hashing produces a fixed '
                                                                     'digest (irreversible)',
                                                                'C': 'Encoding is secure; encryption is insecure; '
                                                                     'hashing requires a key — encoding provides no '
                                                                     "security — it's just format conversion",
                                                                'D': 'Encoding uses keys; encryption uses algorithms; '
                                                                     'hashing uses salts — encoding has no key, '
                                                                     'encryption has a key, hashing can use a salt '
                                                                     "(but the salt isn't a key in the encryption "
                                                                     'sense)'},
                                                 'question': 'What is the difference between encoding, encryption, and '
                                                             'hashing?',
                                                 'wrong_explanations': {   'A': 'They serve fundamentally different '
                                                                                'purposes.',
                                                                           'C': "Encoding provides no security — it's "
                                                                                'just format conversion.',
                                                                           'D': 'Encoding has no key, encryption has a '
                                                                                'key, hashing can use a salt (but the '
                                                                                "salt isn't a key in the encryption "
                                                                                'sense).'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Rainbow tables contain pre-computed hash values for '
                                                                'millions of possible passwords — allowing attackers '
                                                                'to look up a hash and find the plaintext. Salting '
                                                                'defeats this because each hash is unique, making '
                                                                'pre-computation impractical.',
                                                 'options': {   'A': 'An attack using colourful phishing emails; '
                                                                     'countered by email filters — colourful phishing '
                                                                     "is not a rainbow table attack — it's purely a "
                                                                     'cryptographic concept',
                                                                'B': 'A pre-computed table of hash values for common '
                                                                     'passwords used to crack hashes; countered by '
                                                                     'salting',
                                                                'C': 'A brute-force attack on encrypted files; '
                                                                     'countered by longer passwords — rainbow tables '
                                                                     'specifically target hash lookups — brute-force '
                                                                     'attacks differ',
                                                                'D': 'An SQL injection attack using encoded '
                                                                     'characters; countered by input validation'},
                                                 'question': "What is a 'rainbow table' attack and how is it "
                                                             'countered?',
                                                 'wrong_explanations': {   'A': 'Colourful phishing is not a rainbow '
                                                                                "table attack — it's purely a "
                                                                                'cryptographic concept.',
                                                                           'C': 'Rainbow tables specifically target '
                                                                                'hash lookups — brute-force attacks '
                                                                                'differ.',
                                                                           'D': 'SQL injection is a completely '
                                                                                'different attack type.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The birthday paradox shows collisions are far more '
                                                                'likely than expected. A birthday attack exploits this '
                                                                'to find two different inputs with the same hash — '
                                                                'breaking digital signatures and data integrity '
                                                                'checks.',
                                                 'options': {   'A': 'An attack exploiting birthday-related social '
                                                                     'engineering — birthday attacks are purely '
                                                                     'mathematical — not social engineering',
                                                                'B': 'An attack exploiting the probability that two '
                                                                     'different inputs will produce the same hash '
                                                                     '(collision), which is higher than expected due '
                                                                     'to the birthday paradox',
                                                                'C': 'An attack that times out authentication after '
                                                                     "the user's birthday — there is no authentication "
                                                                     'timeout related to birthdays',
                                                                'D': 'Guessing passwords based on birthdate patterns — '
                                                                     'using birthdate patterns to guess passwords is a '
                                                                     'common cracking technique but not a birthday '
                                                                     'attack'},
                                                 'question': "What is a 'birthday attack' in cryptography?",
                                                 'wrong_explanations': {   'A': 'Birthday attacks are purely '
                                                                                'mathematical — not social '
                                                                                'engineering.',
                                                                           'C': 'There is no authentication timeout '
                                                                                'related to birthdays.',
                                                                           'D': 'Using birthdate patterns to guess '
                                                                                'passwords is a common cracking '
                                                                                'technique but not a birthday '
                                                                                'attack.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Steganography hides data inside cover files — e.g., '
                                                                'embedding text in image pixels (LSB steganography). '
                                                                'Unlike encryption (hides what data says), '
                                                                'steganography hides that data exists.',
                                                 'options': {   'A': 'Encrypting text using a stenography technique — '
                                                                     'steganography and stenography are different — '
                                                                     'stenography is shorthand writing',
                                                                'B': 'Hiding secret data within ordinary-looking files '
                                                                     '(images, audio, video) without altering the '
                                                                     'apparent content',
                                                                'C': 'A type of authentication using graphical '
                                                                     'patterns — graphical pattern authentication is '
                                                                     'graphical passwords — not steganography',
                                                                'D': 'Encoding data using Morse code — morse code is a '
                                                                     'specific encoding scheme — not steganography'},
                                                 'question': 'What is steganography?',
                                                 'wrong_explanations': {   'A': 'Steganography and stenography are '
                                                                                'different — stenography is shorthand '
                                                                                'writing.',
                                                                           'C': 'Graphical pattern authentication is '
                                                                                'graphical passwords — not '
                                                                                'steganography.',
                                                                           'D': 'Morse code is a specific encoding '
                                                                                'scheme — not steganography.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Self-signed certificates provide encryption but '
                                                                'browsers display warnings because no trusted CA '
                                                                'vouched for the identity. Suitable for internal '
                                                                'use/dev environments, not for public-facing '
                                                                'production sites.',
                                                 'options': {   'A': 'A certificate signed by yourself — fully trusted '
                                                                     'by all browsers by default — self-signed '
                                                                     'certificates are NOT trusted by default — '
                                                                     'browsers show security warnings',
                                                                'B': 'A certificate where the issuer and subject are '
                                                                     'the same entity — not trusted by browsers by '
                                                                     'default because no third-party CA verified the '
                                                                     'identity',
                                                                'C': 'A certificate used for code signing only — code '
                                                                     'signing certificates can be CA-issued or '
                                                                     'self-signed — not exclusive to code signing',
                                                                'D': 'A certificate generated on the fly for each '
                                                                     'connection — per-connection certificates '
                                                                     'describe ephemeral certificates — not '
                                                                     'self-signed specifically'},
                                                 'question': "What is a 'self-signed certificate' and what is its "
                                                             'security limitation?',
                                                 'wrong_explanations': {   'A': 'Self-signed certificates are NOT '
                                                                                'trusted by default — browsers show '
                                                                                'security warnings.',
                                                                           'C': 'Code signing certificates can be '
                                                                                'CA-issued or self-signed — not '
                                                                                'exclusive to code signing.',
                                                                           'D': 'Per-connection certificates describe '
                                                                                'ephemeral certificates — not '
                                                                                'self-signed specifically.'}},
                                             {   'correct': 'B',
                                                 'explanation': "E2EE means messages are encrypted on the sender's "
                                                                "device and only decrypted on the recipient's device — "
                                                                'the service provider sees only ciphertext. Used in '
                                                                'Signal, WhatsApp, and iMessage (when not backed up).',
                                                 'options': {   'A': 'Encryption at both ends of a data centre — data '
                                                                     "centre endpoints are not what 'end-to-end' "
                                                                     'refers to in E2EE',
                                                                'B': 'Only the communicating users can read the '
                                                                     'messages — the service provider cannot decrypt '
                                                                     'them even if it wanted to',
                                                                'C': 'Encryption of data from database to application '
                                                                     '— database-to-application encryption is transit '
                                                                     'encryption within a system, not E2EE',
                                                                'D': 'Encrypting both the header and body of network '
                                                                     'packets — encrypting packet headers and bodies '
                                                                     'is standard transport encryption — E2EE '
                                                                     'specifically excludes intermediaries'},
                                                 'question': "What does 'end-to-end encryption' (E2EE) mean?",
                                                 'wrong_explanations': {   'A': 'Data centre endpoints are not what '
                                                                                "'end-to-end' refers to in E2EE.",
                                                                           'C': 'Database-to-application encryption is '
                                                                                'transit encryption within a system, '
                                                                                'not E2EE.',
                                                                           'D': 'Encrypting packet headers and bodies '
                                                                                'is standard transport encryption — '
                                                                                'E2EE specifically excludes '
                                                                                'intermediaries.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Encryption is only as strong as its key management. '
                                                                'Keys must be generated securely, stored safely '
                                                                '(HSMs), distributed carefully, rotated regularly, and '
                                                                'revoked when compromised — otherwise attackers obtain '
                                                                'the key and bypass encryption.',
                                                 'options': {   'A': 'Managing passwords for user accounts — user '
                                                                     'account passwords are managed by '
                                                                     'identity/password management systems',
                                                                'B': 'The processes for generating, storing, '
                                                                     'distributing, rotating, and revoking '
                                                                     'cryptographic keys — poor key management defeats '
                                                                     'even strong encryption',
                                                                'C': 'Managing physical security keys and access cards '
                                                                     '— physical key management is a physical security '
                                                                     'function',
                                                                'D': 'A key performance indicator (KPI) management '
                                                                     'system — kPI management is a business '
                                                                     'performance concept unrelated to cryptography'},
                                                 'question': "What is 'key management' and why is it critical?",
                                                 'wrong_explanations': {   'A': 'User account passwords are managed by '
                                                                                'identity/password management systems.',
                                                                           'C': 'Physical key management is a physical '
                                                                                'security function.',
                                                                           'D': 'KPI management is a business '
                                                                                'performance concept unrelated to '
                                                                                'cryptography.'}},
                                             {   'correct': 'A',
                                                 'explanation': "SHA-1 produces 160-bit hashes. In 2017, Google's "
                                                                'SHAttered project demonstrated a practical SHA-1 '
                                                                'collision. Browsers have moved to SHA-256+ for '
                                                                'certificates — SHA-1 TLS certificates are now '
                                                                'rejected.',
                                                 'options': {   'A': 'A 160-bit hash function deprecated because '
                                                                     'collisions were demonstrated, making it '
                                                                     'unsuitable for certificates and digital '
                                                                     'signatures',
                                                                'B': 'A symmetric encryption algorithm deprecated due '
                                                                     'to key length — sHA-1 is a hash function, not a '
                                                                     'symmetric encryption algorithm',
                                                                'C': 'A 128-bit hash function deprecated because it '
                                                                     'was too slow — sHA-1 was deprecated due to '
                                                                     'collision vulnerabilities, not speed issues',
                                                                'D': 'An asymmetric algorithm deprecated because '
                                                                     'quantum computers can break it — quantum '
                                                                     "vulnerability is a concern for SHA-1's successor "
                                                                     'SHA-256 in future — SHA-1 was broken '
                                                                     'classically'},
                                                 'question': 'What is SHA-1 and why is it deprecated?',
                                                 'wrong_explanations': {   'B': 'SHA-1 is a hash function, not a '
                                                                                'symmetric encryption algorithm.',
                                                                           'C': 'SHA-1 was deprecated due to collision '
                                                                                'vulnerabilities, not speed issues.',
                                                                           'D': 'Quantum vulnerability is a concern '
                                                                                "for SHA-1's successor SHA-256 in "
                                                                                'future — SHA-1 was broken '
                                                                                'classically.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'bcrypt is slow by design (configurable cost factor) — '
                                                                'making brute-force attacks expensive. It '
                                                                'automatically generates and stores a salt per '
                                                                'password, preventing rainbow table attacks. Preferred '
                                                                'over plain SHA/MD5 for passwords.',
                                                 'options': {   'A': 'An encryption algorithm for protecting password '
                                                                     'databases — bcrypt is a hashing algorithm, not '
                                                                     'encryption — password hashes cannot be decrypted',
                                                                'B': 'A purpose-built password hashing algorithm that '
                                                                     'is deliberately slow and includes a built-in '
                                                                     'salt — resistant to brute-force and rainbow '
                                                                     'table attacks',
                                                                'C': 'A hashing algorithm producing 512-bit outputs — '
                                                                     'bcrypt produces 60-character encoded output — '
                                                                     'not specifically 512 bits like SHA-512',
                                                                'D': 'A digital signature algorithm for verifying user '
                                                                     'passwords — bcrypt verifies passwords by '
                                                                     're-hashing and comparing — not digital '
                                                                     'signatures'},
                                                 'question': 'What is bcrypt and why is it preferred for password '
                                                             'storage?',
                                                 'wrong_explanations': {   'A': 'bcrypt is a hashing algorithm, not '
                                                                                'encryption — password hashes cannot '
                                                                                'be decrypted.',
                                                                           'C': 'bcrypt produces 60-character encoded '
                                                                                'output — not specifically 512 bits '
                                                                                'like SHA-512.',
                                                                           'D': 'bcrypt verifies passwords by '
                                                                                're-hashing and comparing — not '
                                                                                'digital signatures.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'CRLs (and the newer OCSP) allow browsers to check if '
                                                                'a certificate has been revoked — e.g., if a private '
                                                                'key was compromised. Without checking, a stolen '
                                                                'certificate could be used fraudulently.',
                                                 'options': {   'A': 'A list of expired SSL certificates — expired '
                                                                     'certificates are simply not valid — revocation '
                                                                     'is for certificates invalidated before expiry',
                                                                'B': 'A list published by a CA of certificates it has '
                                                                     'revoked before their expiry date — browsers '
                                                                     'check this to avoid trusting compromised '
                                                                     'certificates',
                                                                'C': 'A blacklist of malicious websites — website '
                                                                     'blacklists are maintained by browsers/security '
                                                                     'vendors — not CRLs',
                                                                'D': 'A list of weak cryptographic algorithms to avoid '
                                                                     '— algorithm deprecation lists are separate '
                                                                     'security guidance — not CRLs'},
                                                 'question': "What is a 'certificate revocation list' (CRL)?",
                                                 'wrong_explanations': {   'A': 'Expired certificates are simply not '
                                                                                'valid — revocation is for '
                                                                                'certificates invalidated before '
                                                                                'expiry.',
                                                                           'C': 'Website blacklists are maintained by '
                                                                                'browsers/security vendors — not CRLs.',
                                                                           'D': 'Algorithm deprecation lists are '
                                                                                'separate security guidance — not '
                                                                                'CRLs.'}},
                                             {   'correct': 'A',
                                                 'explanation': 'Encryption at rest protects data stored on '
                                                                'disks/databases (e.g., BitLocker, database '
                                                                'encryption). Encryption in transit protects data '
                                                                'moving over networks (e.g., TLS/HTTPS). Both are '
                                                                'needed for complete protection.',
                                                 'options': {   'A': 'Encryption at rest protects stored data; '
                                                                     'encryption in transit protects data being sent '
                                                                     'over a network',
                                                                'B': 'Encryption at rest is for old data; encryption '
                                                                     'in transit is for new data — age of data is '
                                                                     'irrelevant — the distinction is storage vs '
                                                                     'transmission',
                                                                'C': 'Encryption at rest uses asymmetric keys; '
                                                                     'encryption in transit uses symmetric keys',
                                                                'D': 'They are the same technique applied at different '
                                                                     'network layers — they are distinct concepts '
                                                                     'addressing different threat scenarios'},
                                                 'question': "What is 'encryption at rest' vs 'encryption in transit'?",
                                                 'wrong_explanations': {   'B': 'Age of data is irrelevant — the '
                                                                                'distinction is storage vs '
                                                                                'transmission.',
                                                                           'C': 'Both can use symmetric keys — the '
                                                                                'distinction is where data is being '
                                                                                'protected.',
                                                                           'D': 'They are distinct concepts addressing '
                                                                                'different threat scenarios.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'A hash collision is when two different inputs produce '
                                                                'identical hash outputs. Good hash functions are '
                                                                'collision-resistant — collisions should be '
                                                                'computationally infeasible to find. MD5 and SHA-1 '
                                                                'have known collisions.',
                                                 'options': {   'A': 'When two hash functions produce the same output '
                                                                     'size',
                                                                'B': 'When two different inputs produce the same hash '
                                                                     'output',
                                                                'C': 'When a hash function fails to process input',
                                                                'D': 'When an attacker reverses a hash to find the '
                                                                     'original input'},
                                                 'question': "What is a 'hash collision'?",
                                                 'wrong_explanations': {   'A': 'Two hash functions having the same '
                                                                                'output size is coincidental, not a '
                                                                                'collision.',
                                                                           'C': 'Hash function failures are '
                                                                                'implementation bugs — not collisions.',
                                                                           'D': 'Reversing a hash to find input is a '
                                                                                "'preimage attack' — different from "
                                                                                'finding a collision.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The TLS handshake: (1) Client hello (supported '
                                                                'ciphers), (2) Server hello + certificate, (3) Key '
                                                                'exchange, (4) Session keys derived. After the '
                                                                'handshake, all data is encrypted with the negotiated '
                                                                'symmetric session key.',
                                                 'options': {   'A': 'A physical security check when accessing a data '
                                                                     'centre — the TLS handshake is a protocol '
                                                                     'process, not a physical security measure',
                                                                'B': 'The initial negotiation between client and '
                                                                     'server to agree on cryptographic parameters, '
                                                                     'authenticate the server, and establish session '
                                                                     'keys before transmitting data',
                                                                'C': 'A command used to verify network connectivity — '
                                                                     "'Handshake' in TCP/IP refers to the TCP "
                                                                     'three-way handshake — TLS handshake is different '
                                                                     'and more complex',
                                                                'D': 'A digital signature exchanged between two '
                                                                     'parties — a digital signature is one component '
                                                                     'of the TLS handshake, not the handshake itself'},
                                                 'question': "In the context of TLS, what is a 'handshake'?",
                                                 'wrong_explanations': {   'A': 'The TLS handshake is a protocol '
                                                                                'process, not a physical security '
                                                                                'measure.',
                                                                           'C': "'Handshake' in TCP/IP refers to the "
                                                                                'TCP three-way handshake — TLS '
                                                                                'handshake is different and more '
                                                                                'complex.',
                                                                           'D': 'A digital signature is one component '
                                                                                'of the TLS handshake, not the '
                                                                                'handshake itself.'}}],
    'Week 5 - Web Application Security': [   {   'correct': 'C',
                                                 'explanation': 'XSS injects malicious client-side scripts (usually '
                                                                'JavaScript) into web pages. When viewed by others, '
                                                                'the script executes in their browser context.',
                                                 'options': {   'A': 'SQL Injection',
                                                                'B': 'CSRF',
                                                                'C': 'Cross-Site Scripting (XSS)',
                                                                'D': 'Session Hijacking'},
                                                 'question': 'What attack involves injecting malicious scripts into '
                                                             'web pages viewed by other users?',
                                                 'wrong_explanations': {   'A': 'SQL Injection targets database '
                                                                                'queries.',
                                                                           'B': 'CSRF tricks authenticated users into '
                                                                                'performing unintended actions.',
                                                                           'D': 'Session hijacking steals session '
                                                                                'tokens to impersonate users.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'HTTP is stateless — each request is independent. '
                                                                'Cookies are name/value pairs stored in the browser '
                                                                'that add state, enabling session management and user '
                                                                'recognition.',
                                                 'options': {   'A': 'To encrypt communications',
                                                                'B': 'To store state since HTTP is stateless',
                                                                'C': 'To compress web page data',
                                                                'D': 'To authenticate the server to the client'},
                                                 'question': 'Why are cookies used in web applications?',
                                                 'wrong_explanations': {   'A': 'HTTPS/TLS handles encryption, not '
                                                                                'cookies.',
                                                                           'C': 'Compression is handled by '
                                                                                'gzip/Brotli, not cookies.',
                                                                           'D': 'Server authentication is handled by '
                                                                                'SSL/TLS certificates.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'An origin is defined by domain name + protocol + '
                                                                'port. ALL THREE must be identical for two resources '
                                                                'to be considered the same origin.',
                                                 'options': {   'A': 'Domain name only',
                                                                'B': 'IP address only',
                                                                'C': 'Domain name + protocol + port',
                                                                'D': 'Domain name + user account'},
                                                 'question': "What defines an 'origin' in the Same Origin Policy?",
                                                 'wrong_explanations': {   'A': 'Domain alone is insufficient — '
                                                                                'protocol and port also matter.',
                                                                           'B': 'IP address is not part of the origin '
                                                                                'definition.',
                                                                           'D': 'User accounts are NOT security '
                                                                                'principals in the Same Origin '
                                                                                'Policy.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'SOP isolates scripts and resources from different '
                                                                'origins. For example, evil.org scripts cannot access '
                                                                'bank.com resources — this is the basic browser '
                                                                'security model.',
                                                 'options': {   'A': 'All cross-origin HTTP requests — sOP restricts '
                                                                     'access/reading, not all requests — CORS allows '
                                                                     'controlled cross-origin sharing',
                                                                'B': 'Scripts from one origin accessing resources of a '
                                                                     'different origin (e.g., evil.org accessing '
                                                                     'bank.com)',
                                                                'C': 'Users logging into multiple websites at once — '
                                                                     'sOP does not prevent multi-site logins',
                                                                'D': 'Cookies being sent over unencrypted connections '
                                                                     '— the Secure flag on cookies handles HTTPS-only '
                                                                     'transmission, not SOP'},
                                                 'question': 'What does the Same Origin Policy (SOP) prevent?',
                                                 'wrong_explanations': {   'A': 'SOP restricts access/reading, not all '
                                                                                'requests — CORS allows controlled '
                                                                                'cross-origin sharing.',
                                                                           'C': 'SOP does not prevent multi-site '
                                                                                'logins.',
                                                                           'D': 'The Secure flag on cookies handles '
                                                                                'HTTPS-only transmission, not SOP.'}},
                                             {   'correct': 'D',
                                                 'explanation': 'GET retrieves resources (HTML, images, CSS) and '
                                                                'appends data to the URL. It should NOT be used for '
                                                                'sensitive data as URLs can be logged/cached.',
                                                 'options': {'A': 'POST', 'B': 'PUT', 'C': 'HEAD', 'D': 'GET'},
                                                 'question': 'Which HTTP method retrieves a resource and sends data in '
                                                             'the URL?',
                                                 'wrong_explanations': {   'A': 'POST sends data in the request body — '
                                                                                'used for form submission and login.',
                                                                           'B': 'PUT updates an existing resource.',
                                                                           'C': 'HEAD retrieves only headers without '
                                                                                'the response body.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'CSRF tricks a logged-in user into submitting a forged '
                                                                'request (e.g., by visiting a malicious page). The '
                                                                'server sees a valid authenticated request and '
                                                                'executes it.',
                                                 'options': {   'A': 'Injecting scripts into web pages — injecting '
                                                                     'scripts into pages is XSS',
                                                                'B': 'Tricking an authenticated user into unknowingly '
                                                                     'sending a malicious request to a site they are '
                                                                     'logged into',
                                                                'C': "Stealing a user's session token — stealing "
                                                                     'session tokens is session hijacking',
                                                                'D': 'Injecting malicious SQL into a database query — '
                                                                     'injecting SQL is SQL injection'},
                                                 'question': 'What is Cross-Site Request Forgery (CSRF)?',
                                                 'wrong_explanations': {   'A': 'Injecting scripts into pages is XSS.',
                                                                           'C': 'Stealing session tokens is session '
                                                                                'hijacking.',
                                                                           'D': 'Injecting SQL is SQL injection.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The XML-RPC interface (/xmlrpc.php) allows multiple '
                                                                'auth attempts per request, making brute-force attacks '
                                                                'significantly faster than attacking wp-login.php '
                                                                'directly.',
                                                 'options': {   'A': 'wp-admin dashboard',
                                                                'B': 'Exposed XML-RPC interface',
                                                                'C': 'Open FTP port',
                                                                'D': 'Default phpMyAdmin page'},
                                                 'question': 'In the WPScan lab (Week 5), which exposed interface made '
                                                             'brute-forcing near-instant?',
                                                 'wrong_explanations': {   'A': 'wp-admin restricts one attempt per '
                                                                                'request — much slower to brute-force.',
                                                                           'C': 'FTP was not identified in this scan.',
                                                                           'D': 'phpMyAdmin was not mentioned in the '
                                                                                'Week 5 lab findings.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'WPScan v3.8.28 is a WordPress-specific scanner used '
                                                                'to enumerate plugins, themes, users, and perform '
                                                                'dictionary attacks on WordPress logins.',
                                                 'options': {   'A': 'Nmap',
                                                                'B': 'Metasploit',
                                                                'C': 'WPScan',
                                                                'D': 'Nessus'},
                                                 'question': 'Which tool was used in Week 5 to perform WordPress '
                                                             'plugin enumeration and dictionary attacks?',
                                                 'wrong_explanations': {   'A': 'Nmap is a general-purpose '
                                                                                'network/port scanner.',
                                                                           'B': 'Metasploit is an exploitation '
                                                                                'framework.',
                                                                           'D': 'Nessus was used in the Week 9 '
                                                                                'vulnerability scanning lab.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'After login, the server generates an authenticator '
                                                                '(session ID) and sends it in a cookie. Each '
                                                                'subsequent request includes this cookie, which the '
                                                                'server verifies. Authenticators must be unforgeable '
                                                                'and tamper-proof.',
                                                 'options': {   'A': "By the user's IP address — iP addresses change "
                                                                     '(NAT, mobile) — unreliable for session '
                                                                     'management',
                                                                'B': 'By re-sending credentials with every request',
                                                                'C': 'By an authenticator cookie that the server '
                                                                     'verifies',
                                                                'D': "By the user's MAC address — mAC addresses are "
                                                                     'only visible on local networks and can be '
                                                                     'spoofed'},
                                                 'question': 'After successful login, how does a server recognise an '
                                                             'authenticated user in subsequent requests?',
                                                 'wrong_explanations': {   'A': 'IP addresses change (NAT, mobile) — '
                                                                                'unreliable for session management.',
                                                                           'B': 'Re-sending credentials with every '
                                                                                'request is insecure.',
                                                                           'D': 'MAC addresses are only visible on '
                                                                                'local networks and can be spoofed.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Broken access control is a key web application '
                                                                'threat. Others include: injection attacks (SQLi, '
                                                                'XSS), broken authentication, sensitive data exposure, '
                                                                'CSRF, insufficient logging, and security '
                                                                'misconfiguration.',
                                                 'options': {   'A': 'ARP poisoning',
                                                                'B': 'Broken access control',
                                                                'C': 'Bluetooth hijacking',
                                                                'D': 'Physical server theft'},
                                                 'question': 'Which of the following is a key threat to web '
                                                             'applications listed in the Week 5 lecture?',
                                                 'wrong_explanations': {   'A': 'ARP poisoning is a network-layer '
                                                                                'attack, not a web application threat.',
                                                                           'C': 'Bluetooth hijacking is a wireless '
                                                                                'proximity attack, not a web threat.',
                                                                           'D': 'Physical theft is a physical security '
                                                                                'concern, not a web application '
                                                                                'threat.'}},
                                             {   'correct': 'C',
                                                 'explanation': "The lecture states: 'Authenticators must be "
                                                                'unforgeable and tamper-proof — malicious clients '
                                                                "shouldn't be able to modify an existing "
                                                                "authenticator.' This prevents session hijacking and "
                                                                'forgery.',
                                                 'options': {   'A': 'Encrypted with AES-256',
                                                                'B': 'Stored in localStorage instead of cookies',
                                                                'C': 'Unforgeable and tamper-proof',
                                                                'D': 'Regenerated every 30 seconds'},
                                                 'question': 'What must cookie authenticators be to prevent session '
                                                             'forgery?',
                                                 'wrong_explanations': {   'A': "AES encryption alone doesn't prevent "
                                                                                'forgery without signing/HMAC.',
                                                                           'B': 'localStorage is actually MORE '
                                                                                'vulnerable to XSS than HttpOnly '
                                                                                'cookies.',
                                                                           'D': "Regeneration every 30 seconds isn't "
                                                                                'the stated requirement.'}},
                                             {   'correct': 'C',
                                                 'explanation': 'Sensitive Data Exposure occurs when an application '
                                                                'inadvertently reveals sensitive data (e.g., leaving '
                                                                'API keys in source code, serving data over HTTP '
                                                                'instead of HTTPS, or poor error messages revealing '
                                                                'system details).',
                                                 'options': {   'A': 'Accessing an admin panel without authentication '
                                                                     '— accessing admin without authentication is '
                                                                     'Broken Access Control',
                                                                'B': 'Injecting SQL to dump a database — dumping a '
                                                                     'database via SQL is SQL Injection',
                                                                'C': 'Inadvertently revealing sensitive information '
                                                                     'such as API keys, passwords, or PII',
                                                                'D': 'Flooding a server with requests — flooding a '
                                                                     'server is a Denial of Service (DoS) attack'},
                                                 'question': "What is 'Sensitive Data Exposure' as a web application "
                                                             'threat?',
                                                 'wrong_explanations': {   'A': 'Accessing admin without '
                                                                                'authentication is Broken Access '
                                                                                'Control.',
                                                                           'B': 'Dumping a database via SQL is SQL '
                                                                                'Injection.',
                                                                           'D': 'Flooding a server is a Denial of '
                                                                                'Service (DoS) attack.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'SQL Injection inserts malicious SQL code into input '
                                                                "fields (e.g., login forms) so the application's "
                                                                'database query is altered — this can bypass '
                                                                'authentication, dump the database, or delete records.',
                                                 'options': {   'A': 'Injecting JavaScript into a webpage to steal '
                                                                     'cookies — injecting JavaScript to steal cookies '
                                                                     'is XSS, not SQL Injection',
                                                                'B': 'Inserting malicious SQL code into an input field '
                                                                     'to manipulate the database query',
                                                                'C': 'Intercepting database traffic on the network — '
                                                                     'intercepting traffic is a Man-in-the-Middle '
                                                                     'attack',
                                                                'D': 'Guessing a database admin password by '
                                                                     'brute-force — brute-forcing a password is a '
                                                                     'different attack — SQLi manipulates query logic'},
                                                 'question': 'What is SQL Injection (SQLi)?',
                                                 'wrong_explanations': {   'A': 'Injecting JavaScript to steal cookies '
                                                                                'is XSS, not SQL Injection.',
                                                                           'C': 'Intercepting traffic is a '
                                                                                'Man-in-the-Middle attack.',
                                                                           'D': 'Brute-forcing a password is a '
                                                                                'different attack — SQLi manipulates '
                                                                                'query logic.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The HttpOnly flag prevents client-side JavaScript '
                                                                'from accessing the cookie. This protects session '
                                                                'cookies from being stolen via XSS attacks that inject '
                                                                'malicious scripts.',
                                                 'options': {   'A': 'Forces the cookie to be sent only over HTTPS — '
                                                                     'the Secure flag forces HTTPS-only transmission — '
                                                                     'not HttpOnly',
                                                                'B': 'Prevents JavaScript from accessing the cookie, '
                                                                     'reducing XSS risk',
                                                                'C': 'Makes the cookie permanent (never expires) — '
                                                                     'cookie expiry is set by the Expires/Max-Age '
                                                                     'attribute',
                                                                'D': 'Restricts the cookie to a specific subdomain — '
                                                                     'domain restriction is set by the Domain '
                                                                     'attribute'},
                                                 'question': 'What does the HttpOnly cookie flag do?',
                                                 'wrong_explanations': {   'A': 'The Secure flag forces HTTPS-only '
                                                                                'transmission — not HttpOnly.',
                                                                           'C': 'Cookie expiry is set by the '
                                                                                'Expires/Max-Age attribute.',
                                                                           'D': 'Domain restriction is set by the '
                                                                                'Domain attribute.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'The Secure flag ensures the cookie is only '
                                                                'transmitted over HTTPS. Without it, a cookie could be '
                                                                'sent over HTTP and intercepted by an attacker on the '
                                                                'network.',
                                                 'options': {   'A': 'Encrypts the cookie value — the Secure flag does '
                                                                     'not encrypt the cookie value — it only controls '
                                                                     'the transport',
                                                                'B': 'Ensures the cookie is only sent over encrypted '
                                                                     'HTTPS connections, not plain HTTP',
                                                                'C': 'Marks the cookie as read-only — there is no '
                                                                     'read-only flag for cookies',
                                                                'D': 'Restricts the cookie to same-site requests only '
                                                                     '— same-site restriction is controlled by the '
                                                                     'SameSite attribute'},
                                                 'question': 'What is the Secure cookie flag?',
                                                 'wrong_explanations': {   'A': 'The Secure flag does not encrypt the '
                                                                                'cookie value — it only controls the '
                                                                                'transport.',
                                                                           'C': 'There is no read-only flag for '
                                                                                'cookies.',
                                                                           'D': 'Same-site restriction is controlled '
                                                                                'by the SameSite attribute.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'CORS (Cross-Origin Resource Sharing) allows servers '
                                                                'to specify which origins are permitted to access '
                                                                'their resources, enabling controlled cross-origin '
                                                                'requests while maintaining security.',
                                                 'options': {   'A': 'Cookie Origin Restriction System — restricts '
                                                                     'cookie sharing — cookie Origin Restriction '
                                                                     'System is not a real term',
                                                                'B': 'Cross-Origin Resource Sharing — allows servers '
                                                                     'to relax the Same Origin Policy in a controlled '
                                                                     'way',
                                                                'C': 'Content Origin Response Security — encrypts '
                                                                     'cross-domain responses — content Origin Response '
                                                                     'Security is not a real term',
                                                                'D': 'Cross-Origin Request Scanning — detects '
                                                                     'malicious cross-domain requests — cross-Origin '
                                                                     'Request Scanning is not a real term'},
                                                 'question': 'What does CORS stand for and why is it needed?',
                                                 'wrong_explanations': {   'A': 'Cookie Origin Restriction System is '
                                                                                'not a real term.',
                                                                           'C': 'Content Origin Response Security is '
                                                                                'not a real term.',
                                                                           'D': 'Cross-Origin Request Scanning is not '
                                                                                'a real term.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Broken Access Control (#1 in OWASP Top 10 2021) '
                                                                'includes: IDOR (Insecure Direct Object References), '
                                                                'privilege escalation, accessing admin functions '
                                                                'without authorisation, and CORS misconfiguration.',
                                                 'options': {   'A': 'When the access control page is poorly designed '
                                                                     '— uI design issues are separate from access '
                                                                     'control logic flaws',
                                                                'B': 'When users can act outside their intended '
                                                                     'permissions — accessing unauthorised data, '
                                                                     'performing privileged actions, or viewing other '
                                                                     "users' accounts",
                                                                'C': "When a website's login page is broken — a broken "
                                                                     'login page is an authentication issue — broken '
                                                                     'access control is about what happens after '
                                                                     'authentication',
                                                                'D': 'When access control lists are misconfigured on a '
                                                                     'firewall — firewall ACLs are network-level '
                                                                     'controls — OWASP Top 10 focuses on '
                                                                     'application-level vulnerabilities'},
                                                 'question': "What is 'Broken Access Control' (OWASP Top 10 #1)?",
                                                 'wrong_explanations': {   'A': 'UI design issues are separate from '
                                                                                'access control logic flaws.',
                                                                           'C': 'A broken login page is an '
                                                                                'authentication issue — broken access '
                                                                                'control is about what happens after '
                                                                                'authentication.',
                                                                           'D': 'Firewall ACLs are network-level '
                                                                                'controls — OWASP Top 10 focuses on '
                                                                                'application-level vulnerabilities.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'IDOR occurs when an application uses '
                                                                'user-controllable input directly to access objects '
                                                                'without authorisation checks — e.g., changing an '
                                                                "order ID in the URL to view someone else's order.",
                                                 'options': {   'A': 'An SQL injection that references internal '
                                                                     'database objects — sQL injection uses SQL syntax '
                                                                     'in queries — IDOR manipulates reference values',
                                                                'B': 'A vulnerability where an attacker can access '
                                                                     'objects (files, data, accounts) by modifying a '
                                                                     'direct reference in the URL or request — e.g., '
                                                                     'changing ?id=123 to ?id=124 to view another '
                                                                     "user's data",
                                                                'C': 'An insecure API that exposes internal object '
                                                                     'classes — aPI exposure of class names is a '
                                                                     'security misconfiguration, not specifically IDOR',
                                                                'D': 'Accessing internal directories via path '
                                                                     'traversal — path traversal uses ../ sequences to '
                                                                     'navigate directories — similar concept but '
                                                                     'different vector'},
                                                 'question': 'What is an IDOR (Insecure Direct Object Reference)?',
                                                 'wrong_explanations': {   'A': 'SQL injection uses SQL syntax in '
                                                                                'queries — IDOR manipulates reference '
                                                                                'values.',
                                                                           'C': 'API exposure of class names is a '
                                                                                'security misconfiguration, not '
                                                                                'specifically IDOR.',
                                                                           'D': 'Path traversal uses ../ sequences to '
                                                                                'navigate directories — similar '
                                                                                'concept but different vector.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Security misconfiguration is one of the most common '
                                                                'vulnerabilities — examples: default admin credentials '
                                                                'left unchanged, directory listing enabled, verbose '
                                                                'error messages exposing stack traces, unnecessary '
                                                                'ports open.',
                                                 'options': {   'A': 'Using an outdated security framework — outdated '
                                                                     "frameworks relate to 'Vulnerable and Outdated "
                                                                     "Components'",
                                                                'B': 'Insecure default configurations, incomplete '
                                                                     'configurations, open cloud storage, verbose '
                                                                     'error messages revealing sensitive info, or '
                                                                     'unnecessary features enabled',
                                                                'C': 'Failing to encrypt configuration files — '
                                                                     'unencrypted config files are one example of '
                                                                     'misconfiguration but not the full definition',
                                                                'D': 'Misconfiguring firewall rules — firewall '
                                                                     'misconfiguration is one aspect but OWASP focuses '
                                                                     'on application-level configuration'},
                                                 'question': "What is 'security misconfiguration' as an OWASP "
                                                             'vulnerability?',
                                                 'wrong_explanations': {   'A': 'Outdated frameworks relate to '
                                                                                "'Vulnerable and Outdated Components'.",
                                                                           'C': 'Unencrypted config files are one '
                                                                                'example of misconfiguration but not '
                                                                                'the full definition.',
                                                                           'D': 'Firewall misconfiguration is one '
                                                                                'aspect but OWASP focuses on '
                                                                                'application-level configuration.'}},
                                             {   'correct': 'A',
                                                 'explanation': 'Command injection occurs when user input is passed '
                                                                'unsanitised to a system shell — e.g., a web app that '
                                                                "runs 'ping ' + user_input as a shell command can be "
                                                                "exploited with input like '8.8.8.8; rm -rf /'.",
                                                 'options': {   'A': 'An attacker injecting operating system commands '
                                                                     'into an application input, which the server then '
                                                                     'executes',
                                                                'B': 'Injecting SQL commands into a database query — '
                                                                     'injecting SQL into database queries is SQL '
                                                                     'injection, not command injection',
                                                                'C': 'Installing a command-and-control agent on a '
                                                                     'target system — c2 agent installation is a '
                                                                     'post-exploitation activity, not command '
                                                                     'injection',
                                                                'D': 'Injecting JavaScript into a web page — injecting '
                                                                     'JavaScript into web pages is Cross-Site '
                                                                     'Scripting (XSS)'},
                                                 'question': "What is 'command injection'?",
                                                 'wrong_explanations': {   'B': 'Injecting SQL into database queries '
                                                                                'is SQL injection, not command '
                                                                                'injection.',
                                                                           'C': 'C2 agent installation is a '
                                                                                'post-exploitation activity, not '
                                                                                'command injection.',
                                                                           'D': 'Injecting JavaScript into web pages '
                                                                                'is Cross-Site Scripting (XSS).'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Path traversal uses ../ (or encoded variants like '
                                                                '%2e%2e%2f) to navigate up the directory tree — e.g., '
                                                                '/../../../etc/passwd to read system files outside the '
                                                                "web application's intended scope.",
                                                 'options': {   'A': 'An attack that overwhelms server routing tables '
                                                                     '— routing table attacks are network-layer '
                                                                     'attacks — path traversal is application-level',
                                                                'B': 'An attack using ../ sequences in file path '
                                                                     'inputs to access files and directories outside '
                                                                     'the intended web root',
                                                                'C': 'Traversing a network using compromised routers — '
                                                                     'network traversal via routers is lateral '
                                                                     'movement — different concept',
                                                                'D': 'Searching for hidden directories using a web '
                                                                     'scanner — directory enumeration using scanners '
                                                                     'is reconnaissance — path traversal is '
                                                                     'exploitation'},
                                                 'question': "What is 'path traversal' (directory traversal)?",
                                                 'wrong_explanations': {   'A': 'Routing table attacks are '
                                                                                'network-layer attacks — path '
                                                                                'traversal is application-level.',
                                                                           'C': 'Network traversal via routers is '
                                                                                'lateral movement — different concept.',
                                                                           'D': 'Directory enumeration using scanners '
                                                                                'is reconnaissance — path traversal is '
                                                                                'exploitation.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Cryptographic failures (OWASP Top 10 #2) expose '
                                                                'sensitive data due to weak/absent cryptography — '
                                                                'transmitting sensitive data over HTTP, storing '
                                                                'passwords with MD5, using deprecated algorithms, or '
                                                                'not encrypting sensitive databases.',
                                                 'options': {   'A': 'Using outdated TLS versions — outdated TLS is '
                                                                     'one example but cryptographic failure '
                                                                     'encompasses all forms of crypto weakness',
                                                                'B': 'Failures in cryptography that expose sensitive '
                                                                     'data — using weak algorithms (MD5, DES), not '
                                                                     'encrypting data in transit, storing passwords in '
                                                                     'plaintext',
                                                                'C': 'A bug in an encryption library — a library bug '
                                                                     'is a specific technical issue — cryptographic '
                                                                     'failure is a broader class of problem',
                                                                'D': 'Using self-signed certificates — self-signed '
                                                                     'certificates are a trust issue — cryptographic '
                                                                     'failure is about algorithm strength and '
                                                                     'application'},
                                                 'question': "What is 'cryptographic failure' as an OWASP "
                                                             'vulnerability?',
                                                 'wrong_explanations': {   'A': 'Outdated TLS is one example but '
                                                                                'cryptographic failure encompasses all '
                                                                                'forms of crypto weakness.',
                                                                           'C': 'A library bug is a specific technical '
                                                                                'issue — cryptographic failure is a '
                                                                                'broader class of problem.',
                                                                           'D': 'Self-signed certificates are a trust '
                                                                                'issue — cryptographic failure is '
                                                                                'about algorithm strength and '
                                                                                'application.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Injection flaws occur when untrusted data is sent to '
                                                                'an interpreter as part of a command or query. SQL '
                                                                'injection, OS command injection, LDAP injection — all '
                                                                'stem from insufficient input validation.',
                                                 'options': {   'A': 'Installing malware by injecting code into memory '
                                                                     '— memory injection is a malware technique — '
                                                                     'OWASP injection refers to interpreter context',
                                                                'B': 'User-supplied data is interpreted as code or '
                                                                     'commands — includes SQL, OS command, LDAP, NoSQL '
                                                                     'injection when input is not validated',
                                                                'C': 'Injecting network packets to disrupt '
                                                                     'communications — network packet injection is a '
                                                                     'network attack — OWASP injection is '
                                                                     'application-level',
                                                                'D': 'Uploading malicious files to a server — '
                                                                     "malicious file uploads are 'insecure file "
                                                                     "upload' vulnerabilities — not injection"},
                                                 'question': "What is 'injection' as defined by OWASP?",
                                                 'wrong_explanations': {   'A': 'Memory injection is a malware '
                                                                                'technique — OWASP injection refers to '
                                                                                'interpreter context.',
                                                                           'C': 'Network packet injection is a network '
                                                                                'attack — OWASP injection is '
                                                                                'application-level.',
                                                                           'D': "Malicious file uploads are 'insecure "
                                                                                "file upload' vulnerabilities — not "
                                                                                'injection.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Without adequate logging and monitoring, breaches go '
                                                                'undetected for months (average 200+ days). Critical '
                                                                'events — logins, access failures, input validation '
                                                                'failures — must be logged and alerts triggered on '
                                                                'anomalies.',
                                                 'options': {   'A': 'Log files taking up too much disk space — '
                                                                     'storage management is an operational concern — '
                                                                     'OWASP focuses on security impact',
                                                                'B': 'Insufficient logging, monitoring, and alerting — '
                                                                     'allowing attacks to go undetected and giving '
                                                                     'attackers time to achieve objectives',
                                                                'C': 'Using insecure logging protocols — protocol '
                                                                     'security for logs is one aspect but not the core '
                                                                     'definition',
                                                                'D': 'Logging too much sensitive data — logging '
                                                                     'sensitive data is a related concern (log '
                                                                     'injection/exposure) but insufficient logging is '
                                                                     'the OWASP vulnerability'},
                                                 'question': "What is 'security logging and monitoring failures' as an "
                                                             'OWASP vulnerability?',
                                                 'wrong_explanations': {   'A': 'Storage management is an operational '
                                                                                'concern — OWASP focuses on security '
                                                                                'impact.',
                                                                           'C': 'Protocol security for logs is one '
                                                                                'aspect but not the core definition.',
                                                                           'D': 'Logging sensitive data is a related '
                                                                                'concern (log injection/exposure) but '
                                                                                'insufficient logging is the OWASP '
                                                                                'vulnerability.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Stored (Persistent) XSS: attacker submits malicious '
                                                                "script to be stored in the server's database (e.g., "
                                                                "blog comment). Every visitor's browser then executes "
                                                                'it — far more dangerous than Reflected XSS.',
                                                 'options': {   'A': "XSS code stored in the attacker's browser — xSS "
                                                                     'scripts are stored server-side, not in the '
                                                                     "attacker's browser",
                                                                'B': 'Malicious script is permanently stored in the '
                                                                     'server (database) and served to every user who '
                                                                     'views the infected page',
                                                                'C': 'An XSS attack embedded in a URL link — xSS '
                                                                     'embedded in a URL is Reflected XSS — not Stored '
                                                                     'XSS',
                                                                'D': 'XSS code stored in a cookie — xSS stored in '
                                                                     'cookies can be part of DOM-based XSS — Stored '
                                                                     'XSS is database-persisted'},
                                                 'question': "What is a 'Stored XSS' attack?",
                                                 'wrong_explanations': {   'A': 'XSS scripts are stored server-side, '
                                                                                "not in the attacker's browser.",
                                                                           'C': 'XSS embedded in a URL is Reflected '
                                                                                'XSS — not Stored XSS.',
                                                                           'D': 'XSS stored in cookies can be part of '
                                                                                'DOM-based XSS — Stored XSS is '
                                                                                'database-persisted.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Reflected XSS: attacker crafts a malicious URL, '
                                                                'victim clicks it, server echoes the script back in '
                                                                "the response, victim's browser executes it. Requires "
                                                                'tricking the victim into clicking the link.',
                                                 'options': {   'A': "XSS stored in the server's database — xSS stored "
                                                                     'in the database is Stored (Persistent) XSS',
                                                                'B': 'Malicious script is included in a URL, reflected '
                                                                     'off the server in the response, and executed in '
                                                                     "the victim's browser when they click the link",
                                                                'C': 'XSS that modifies the DOM without touching the '
                                                                     'server — xSS that only modifies the DOM without '
                                                                     'server involvement is DOM-based XSS',
                                                                'D': 'An XSS attack that bypasses browser security '
                                                                     'policies — bypassing browser security policies '
                                                                     'is a separate class of attack'},
                                                 'question': "What is 'Reflected XSS'?",
                                                 'wrong_explanations': {   'A': 'XSS stored in the database is Stored '
                                                                                '(Persistent) XSS.',
                                                                           'C': 'XSS that only modifies the DOM '
                                                                                'without server involvement is '
                                                                                'DOM-based XSS.',
                                                                           'D': 'Bypassing browser security policies '
                                                                                'is a separate class of attack.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'CSP is a browser security mechanism delivered as an '
                                                                'HTTP header (Content-Security-Policy). It specifies '
                                                                'trusted sources for scripts — even if XSS code is '
                                                                "injected, the browser won't execute it if its origin "
                                                                "isn't in the whitelist.",
                                                 'options': {   'A': 'A server-side validation mechanism for HTML '
                                                                     'content — cSP is a browser-enforced policy, not '
                                                                     'server-side validation',
                                                                'B': 'An HTTP response header that instructs browsers '
                                                                     'which sources of scripts, styles, and media are '
                                                                     'trusted — blocking scripts from unexpected '
                                                                     'sources',
                                                                'C': 'A firewall rule that blocks XSS patterns — wAF '
                                                                     'rules can block XSS patterns but CSP is a '
                                                                     'browser-level defence via HTTP headers',
                                                                'D': 'An encryption policy for web content — cSP '
                                                                     'controls content sources — not encryption'},
                                                 'question': "What is 'Content Security Policy' (CSP) and how does it "
                                                             'help against XSS?',
                                                 'wrong_explanations': {   'A': 'CSP is a browser-enforced policy, not '
                                                                                'server-side validation.',
                                                                           'C': 'WAF rules can block XSS patterns but '
                                                                                'CSP is a browser-level defence via '
                                                                                'HTTP headers.',
                                                                           'D': 'CSP controls content sources — not '
                                                                                'encryption.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'X-Frame-Options: DENY or SAMEORIGIN prevents your '
                                                                'page from being loaded in an iframe on a malicious '
                                                                'site — protecting against clickjacking attacks where '
                                                                'users are tricked into clicking hidden buttons.',
                                                 'options': {   'A': 'Preventing SQL injection attacks — sQL injection '
                                                                     'prevention requires parameterised queries — not '
                                                                     'HTTP headers',
                                                                'B': 'Preventing clickjacking — blocking the page from '
                                                                     'being embedded in an iframe on another domain',
                                                                'C': 'Enforcing HTTPS for all connections — hTTPS '
                                                                     'enforcement uses the HSTS header '
                                                                     '(Strict-Transport-Security)',
                                                                'D': 'Blocking XSS by restricting JavaScript sources — '
                                                                     'javaScript source restrictions use the '
                                                                     'Content-Security-Policy header'},
                                                 'question': "What is the 'X-Frame-Options' HTTP header used for?",
                                                 'wrong_explanations': {   'A': 'SQL injection prevention requires '
                                                                                'parameterised queries — not HTTP '
                                                                                'headers.',
                                                                           'C': 'HTTPS enforcement uses the HSTS '
                                                                                'header (Strict-Transport-Security).',
                                                                           'D': 'JavaScript source restrictions use '
                                                                                'the Content-Security-Policy header.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'HSTS (Strict-Transport-Security header) instructs '
                                                                'browsers to always use HTTPS for the specified domain '
                                                                "and duration. Once set, browsers won't make plain "
                                                                'HTTP requests — protecting against SSL stripping '
                                                                'attacks.',
                                                 'options': {   'A': 'A protocol that speeds up HTTPS connections — '
                                                                     "hSTS is a security header — it doesn't directly "
                                                                     'speed up connections',
                                                                'B': 'An HTTP header that tells browsers to only '
                                                                     'access the site over HTTPS for a specified '
                                                                     'period — preventing protocol downgrade attacks',
                                                                'C': 'A firewall rule that redirects HTTP to HTTPS — '
                                                                     'hTTP-to-HTTPS redirect is a server-side redirect '
                                                                     '(301) — HSTS makes the browser enforce HTTPS '
                                                                     'itself',
                                                                'D': 'An SSL/TLS extension that encrypts HTTP headers '
                                                                     '— hSTS is a policy header — TLS handles actual '
                                                                     'encryption'},
                                                 'question': "What is 'HSTS' (HTTP Strict Transport Security)?",
                                                 'wrong_explanations': {   'A': 'HSTS is a security header — it '
                                                                                "doesn't directly speed up "
                                                                                'connections.',
                                                                           'C': 'HTTP-to-HTTPS redirect is a '
                                                                                'server-side redirect (301) — HSTS '
                                                                                'makes the browser enforce HTTPS '
                                                                                'itself.',
                                                                           'D': 'HSTS is a policy header — TLS handles '
                                                                                'actual encryption.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Parameterised queries use placeholders for user input '
                                                                '— the database engine treats parameters as data, not '
                                                                'SQL code. This completely prevents SQL injection '
                                                                'regardless of what the user inputs.',
                                                 'options': {   'A': 'Queries with adjustable timeout parameters — '
                                                                     'query timeouts are a performance/reliability '
                                                                     'feature — not parameterisation',
                                                                'B': 'Separating SQL code from data — user input is '
                                                                     'treated as data, not code — preventing SQL '
                                                                     'injection',
                                                                'C': 'Using stored procedures in the database — stored '
                                                                     'procedures can be secure if parameterised but '
                                                                     'they are not the same as parameterised queries',
                                                                'D': 'Caching frequently used queries for performance '
                                                                     '— query caching is a performance optimisation — '
                                                                     'not a security technique'},
                                                 'question': 'What does it mean when a web application uses '
                                                             "'parameterised queries' (prepared statements)?",
                                                 'wrong_explanations': {   'A': 'Query timeouts are a '
                                                                                'performance/reliability feature — not '
                                                                                'parameterisation.',
                                                                           'C': 'Stored procedures can be secure if '
                                                                                'parameterised but they are not the '
                                                                                'same as parameterised queries.',
                                                                           'D': 'Query caching is a performance '
                                                                                'optimisation — not a security '
                                                                                'technique.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Business logic vulnerabilities exploit how an '
                                                                'application is supposed to work — e.g., applying a '
                                                                'discount code multiple times, skipping payment steps, '
                                                                'or modifying prices in hidden form fields.',
                                                 'options': {   'A': 'A vulnerability in business accounting software '
                                                                     '— accounting software vulnerabilities are '
                                                                     'technical bugs — business logic flaws exploit '
                                                                     'intended features',
                                                                'B': 'A flaw in application design where attackers '
                                                                     'exploit the intended functionality in unintended '
                                                                     'ways — bypassing business rules',
                                                                'C': 'A logic error in JavaScript code — javaScript '
                                                                     'bugs are code-level errors — business logic '
                                                                     'flaws are design-level issues',
                                                                'D': 'A vulnerability in business intelligence tools — '
                                                                     'bI tool vulnerabilities are technical — not '
                                                                     'business logic flaws'},
                                                 'question': "What is 'business logic vulnerability'?",
                                                 'wrong_explanations': {   'A': 'Accounting software vulnerabilities '
                                                                                'are technical bugs — business logic '
                                                                                'flaws exploit intended features.',
                                                                           'C': 'JavaScript bugs are code-level errors '
                                                                                '— business logic flaws are '
                                                                                'design-level issues.',
                                                                           'D': 'BI tool vulnerabilities are technical '
                                                                                '— not business logic flaws.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'IDOR prevention requires server-side access control — '
                                                                'never trust the client to enforce access. Even if '
                                                                'object IDs are GUIDs or encrypted, if the server '
                                                                "doesn't check permissions, IDOR exists.",
                                                 'options': {   'A': 'Use POST instead of GET for all requests — using '
                                                                     "POST doesn't prevent IDOR — the attacker can "
                                                                     'still modify POST body parameters',
                                                                'B': 'Enforce server-side authorisation checks on '
                                                                     'every resource access — verify the requesting '
                                                                     'user has permission for the specific object',
                                                                'C': 'Encrypt all object IDs in the URL — encrypting '
                                                                     "IDs makes them harder to guess but doesn't "
                                                                     "prevent IDOR if the server doesn't check "
                                                                     'permissions',
                                                                'D': 'Use GUIDs instead of sequential integers for '
                                                                     'object IDs — gUIDs make ID enumeration harder '
                                                                     "but don't prevent IDOR — access control checks "
                                                                     'are essential'},
                                                 'question': "What is 'Insecure Direct Object Reference' prevention "
                                                             'technique?',
                                                 'wrong_explanations': {   'A': "Using POST doesn't prevent IDOR — the "
                                                                                'attacker can still modify POST body '
                                                                                'parameters.',
                                                                           'C': 'Encrypting IDs makes them harder to '
                                                                                "guess but doesn't prevent IDOR if the "
                                                                                "server doesn't check permissions.",
                                                                           'D': 'GUIDs make ID enumeration harder but '
                                                                                "don't prevent IDOR — access control "
                                                                                'checks are essential.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Input validation is the first line of defence against '
                                                                'injection attacks — validating on both client and '
                                                                'server sides (client-side is bypassed by attackers), '
                                                                'ensuring only expected data enters the system.',
                                                 'options': {   'A': 'Validating that all input is in English — '
                                                                     'language restriction is not input validation — '
                                                                     'it would break international applications',
                                                                'B': 'Checking that user-supplied input conforms to '
                                                                     'expected format, type, and length — rejecting or '
                                                                     'sanitising anything unexpected to prevent '
                                                                     'injection attacks',
                                                                'C': 'Encrypting input data before processing — '
                                                                     "encryption protects data — it doesn't prevent "
                                                                     'malicious input from being processed',
                                                                'D': 'Logging all user inputs for audit purposes — '
                                                                     'logging input helps with monitoring/forensics — '
                                                                     "it doesn't prevent attacks"},
                                                 'question': "What is 'input validation' and why is it a security best "
                                                             'practice?',
                                                 'wrong_explanations': {   'A': 'Language restriction is not input '
                                                                                'validation — it would break '
                                                                                'international applications.',
                                                                           'C': "Encryption protects data — it doesn't "
                                                                                'prevent malicious input from being '
                                                                                'processed.',
                                                                           'D': 'Logging input helps with '
                                                                                "monitoring/forensics — it doesn't "
                                                                                'prevent attacks.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Output encoding converts characters like <, >, \', " '
                                                                'into HTML entities (&lt;, &gt;, etc.) so browsers '
                                                                'display them as text rather than executing them as '
                                                                'HTML/JavaScript — the primary XSS prevention '
                                                                'technique.',
                                                 'options': {   'A': 'Compressing output data for faster transmission '
                                                                     '— compression is a performance optimisation — '
                                                                     'not a security technique',
                                                                'B': 'Converting special characters in output to safe '
                                                                     'representations — preventing browsers from '
                                                                     'interpreting user data as code (preventing XSS)',
                                                                'C': 'Encoding API responses in JSON format — jSON '
                                                                     'encoding is for data format — output encoding '
                                                                     'prevents XSS',
                                                                'D': 'Encrypting data before displaying it to the user '
                                                                     '— encrypting output makes it unreadable — output '
                                                                     'encoding preserves readability while preventing '
                                                                     'script execution'},
                                                 'question': "What is 'output encoding' and why is it used?",
                                                 'wrong_explanations': {   'A': 'Compression is a performance '
                                                                                'optimisation — not a security '
                                                                                'technique.',
                                                                           'C': 'JSON encoding is for data format — '
                                                                                'output encoding prevents XSS.',
                                                                           'D': 'Encrypting output makes it unreadable '
                                                                                '— output encoding preserves '
                                                                                'readability while preventing script '
                                                                                'execution.'}},
                                             {   'correct': 'B',
                                                 'explanation': 'Burp Suite is the standard tool for web app pen '
                                                                'testing — its proxy intercepts requests/responses, '
                                                                'allowing testers to modify parameters, run automated '
                                                                'scans (Intruder, Scanner), test for SQLi/XSS/IDOR, '
                                                                'and replay requests.',
                                                 'options': {   'A': 'Automatically patches web application '
                                                                     'vulnerabilities — burp Suite identifies '
                                                                     'vulnerabilities — patching requires developer '
                                                                     'action',
                                                                'B': 'Acts as a proxy between browser and server — '
                                                                     'allowing interception, inspection, and '
                                                                     'modification of HTTP/HTTPS traffic to test for '
                                                                     'vulnerabilities',
                                                                'C': 'Scans network ports and identifies services — '
                                                                     'network port scanning is done by Nmap — Burp '
                                                                     'Suite focuses on HTTP/HTTPS application traffic',
                                                                'D': 'Monitors web application performance under load '
                                                                     '— load testing is done by tools like JMeter — '
                                                                     'Burp Suite is a security testing proxy'},
                                                 'question': 'What does Burp Suite do in web application security '
                                                             'testing?',
                                                 'wrong_explanations': {   'A': 'Burp Suite identifies vulnerabilities '
                                                                                '— patching requires developer action.',
                                                                           'C': 'Network port scanning is done by Nmap '
                                                                                '— Burp Suite focuses on HTTP/HTTPS '
                                                                                'application traffic.',
                                                                           'D': 'Load testing is done by tools like '
                                                                                'JMeter — Burp Suite is a security '
                                                                                'testing proxy.'}}],
    'Week 7 - Principles of Secure Design': [   {   'correct': 'B',
                                                    'explanation': 'NCSC Five Principles: 1) Establish context, 2) '
                                                                   'Make compromise difficult, 3) Make disruption '
                                                                   'difficult, 4) Make compromise detection easier, 5) '
                                                                   'Reduce the impact of compromise.',
                                                    'options': {   'A': 'Detect, Prevent, Respond, Recover, Identify — '
                                                                        'those are the NIST Cybersecurity Framework '
                                                                        'functions',
                                                                   'B': 'Establish context, Make compromise difficult, '
                                                                        'Make disruption difficult, Make detection '
                                                                        'easier, Reduce impact',
                                                                   'C': 'Confidentiality, Integrity, Availability, '
                                                                        'Authentication, Authorisation — those are '
                                                                        'security properties/controls, not the NCSC '
                                                                        'design principles',
                                                                   'D': 'Plan, Do, Check, Act, Review — '
                                                                        'plan-Do-Check-Act is the PDCA management '
                                                                        'cycle'},
                                                    'question': 'What are the 5 NCSC Secure Design principles in '
                                                                'order?',
                                                    'wrong_explanations': {   'A': 'Those are the NIST Cybersecurity '
                                                                                   'Framework functions.',
                                                                              'C': 'Those are security '
                                                                                   'properties/controls, not the NCSC '
                                                                                   'design principles.',
                                                                              'D': 'Plan-Do-Check-Act is the PDCA '
                                                                                   'management cycle.'}},
                                                {   'correct': 'C',
                                                    'explanation': "'Make Compromise Detection Easier' includes: "
                                                                   'collecting security logs, designing simple '
                                                                   'communication flows, detecting C2 malware '
                                                                   'communications, making monitoring independent, and '
                                                                   "understanding 'normal' to detect abnormal.",
                                                    'options': {   'A': 'Make compromise difficult',
                                                                   'B': 'Make disruption difficult',
                                                                   'C': 'Make compromise detection easier',
                                                                   'D': 'Establish context'},
                                                    'question': 'Which principle involves collecting security logs and '
                                                                'making monitoring independent of the monitored '
                                                                'system?',
                                                    'wrong_explanations': {   'A': "'Make compromise difficult' is "
                                                                                   'about reducing attack surface and '
                                                                                   'validating inputs.',
                                                                              'B': "'Make disruption difficult' is "
                                                                                   'about resilience, scalability, and '
                                                                                   'DoS resistance.',
                                                                              'D': "'Establish context' is about "
                                                                                   'understanding the threat model '
                                                                                   'before designing.'}},
                                                {   'correct': 'C',
                                                    'explanation': 'External input cannot be trusted. The principle '
                                                                   'states it must be transformed, validated, or '
                                                                   'rendered safely to prevent injection attacks (XSS, '
                                                                   'SQL injection, etc.).',
                                                    'options': {   'A': 'Block all external input by default — '
                                                                        'blocking all external input would break web '
                                                                        'applications',
                                                                   'B': 'Log all external input — logging alone '
                                                                        'without validation leaves systems vulnerable',
                                                                   'C': "External input can't be trusted — transform, "
                                                                        'validate, or render it safely',
                                                                   'D': 'Encrypt all external input with AES-256 — '
                                                                        'encryption is not the recommended approach — '
                                                                        'validation and sanitisation are'},
                                                    'question': "What does 'Make Compromise Difficult' say about "
                                                                'external user input?',
                                                    'wrong_explanations': {   'A': 'Blocking all external input would '
                                                                                   'break web applications.',
                                                                              'B': 'Logging alone without validation '
                                                                                   'leaves systems vulnerable.',
                                                                              'D': 'Encryption is not the recommended '
                                                                                   'approach — validation and '
                                                                                   'sanitisation are.'}},
                                                {   'correct': 'C',
                                                    'explanation': "'Reduce the Impact of Compromise' includes network "
                                                                   'segmentation so a breach of one zone cannot easily '
                                                                   'spread. Other measures include separation of '
                                                                   'duties, anonymising exported data, and making '
                                                                   'recovery easy.',
                                                    'options': {   'A': 'Make disruption difficult',
                                                                   'B': 'Establish context',
                                                                   'C': 'Reduce the impact of compromise',
                                                                   'D': 'Make compromise detection easier'},
                                                    'question': "Which principle recommends using a 'zoned or "
                                                                "segmented network approach'?",
                                                    'wrong_explanations': {   'A': "'Make disruption difficult' "
                                                                                   'focuses on availability and DoS '
                                                                                   'resistance.',
                                                                              'B': "'Establish context' is about "
                                                                                   'understanding requirements before '
                                                                                   'designing.',
                                                                              'D': "'Make detection easier' is about "
                                                                                   'logging and monitoring.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Security by Design focuses on prevention rather '
                                                                   'than repair. It embeds security into the '
                                                                   'development lifecycle from the start, rather than '
                                                                   'adding it as an afterthought.',
                                                    'options': {   'A': 'Faster incident response after a breach',
                                                                   'B': 'Prevention rather than repair and restoration',
                                                                   'C': 'Hiring more security staff — staffing levels '
                                                                        'are not the focus',
                                                                   'D': 'Buying the latest security tools — purchasing '
                                                                        'tools is reactive; Security by Design is '
                                                                        'about building security in'},
                                                    'question': "What does 'Security by Design' fundamentally focus "
                                                                'on?',
                                                    'wrong_explanations': {   'A': 'Incident response is reactive — '
                                                                                   'Security by Design is proactive.',
                                                                              'C': 'Staffing levels are not the focus.',
                                                                              'D': 'Purchasing tools is reactive; '
                                                                                   'Security by Design is about '
                                                                                   'building security in.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Failure of security design is caused by: (1) '
                                                                   'Security is deliberately sacrificed, (2) Security '
                                                                   'is not viewed as important, (3) Wrong decisions '
                                                                   'are made during design and implementation.',
                                                    'options': {   'A': 'Using open-source software — open-source '
                                                                        'software is not listed as a cause of design '
                                                                        'failure',
                                                                   'B': 'Security is deliberately sacrificed or not '
                                                                        'viewed as important',
                                                                   'C': 'Deploying virtual machines instead of '
                                                                        'physical servers',
                                                                   'D': 'Using cloud-based infrastructure — cloud '
                                                                        'infrastructure is not listed as a cause'},
                                                    'question': 'What is one of the three causes of failure in system '
                                                                'security design?',
                                                    'wrong_explanations': {   'A': 'Open-source software is not listed '
                                                                                   'as a cause of design failure.',
                                                                              'C': 'Using VMs is not a cause of '
                                                                                   'security design failure.',
                                                                              'D': 'Cloud infrastructure is not listed '
                                                                                   'as a cause.'}},
                                                {   'correct': 'B',
                                                    'explanation': "'Make Disruption Difficult' requires identifying "
                                                                   'where availability depends on third parties and '
                                                                   'planning for their failure — ensuring systems '
                                                                   'remain operational even if a supplier or service '
                                                                   'goes down.',
                                                    'options': {   'A': 'Never use third-party services — avoiding all '
                                                                        'third parties is impractical — the principle '
                                                                        'is to plan for their failure',
                                                                   'B': 'Identify where availability depends on a '
                                                                        'third party and plan for their failure',
                                                                   'C': 'Always use third-party security auditors — '
                                                                        'using third-party auditors is good practice '
                                                                        'but not what this principle states',
                                                                   'D': 'Store all data locally to avoid third-party '
                                                                        'risk — storing everything locally is not the '
                                                                        'solution — resilience planning is'},
                                                    'question': "What does 'Make Disruption Difficult' require "
                                                                'designers to consider regarding third parties?',
                                                    'wrong_explanations': {   'A': 'Avoiding all third parties is '
                                                                                   'impractical — the principle is to '
                                                                                   'plan for their failure.',
                                                                              'C': 'Using third-party auditors is good '
                                                                                   'practice but not what this '
                                                                                   'principle states.',
                                                                              'D': 'Storing everything locally is not '
                                                                                   'the solution — resilience planning '
                                                                                   'is.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'The three aspects of Security Design are: (1) '
                                                                   'Knowledge Security (understanding exploits and '
                                                                   'defences), (2) Reasoning and Decision Making '
                                                                   '(considering security parameters), (3) Knowledge '
                                                                   'of the System (evaluating the security of the '
                                                                   'specific system).',
                                                    'options': {   'A': 'Detection, Prevention, Response — detection, '
                                                                        'Prevention, Response describes incident '
                                                                        'management',
                                                                   'B': 'Knowledge Security, Reasoning and Decision '
                                                                        'Making, Knowledge of the System',
                                                                   'C': 'Confidentiality, Integrity, Availability — '
                                                                        'cIA Triad describes security properties, not '
                                                                        'aspects of Security Design',
                                                                   'D': 'Policies, Standards, Procedures — policies, '
                                                                        'Standards, Procedures is the IT security '
                                                                        'policy framework'},
                                                    'question': 'What are the three aspects of Security Design '
                                                                'mentioned in the lecture?',
                                                    'wrong_explanations': {   'A': 'Detection, Prevention, Response '
                                                                                   'describes incident management.',
                                                                              'C': 'CIA Triad describes security '
                                                                                   'properties, not aspects of '
                                                                                   'Security Design.',
                                                                              'D': 'Policies, Standards, Procedures is '
                                                                                   'the IT security policy '
                                                                                   'framework.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'OWASP Juice Shop is used to highlight trade-offs '
                                                                   'between usability and security, show real-world '
                                                                   'failures of secure design, demonstrate threats and '
                                                                   'vulnerabilities, and reinforce why security must '
                                                                   'be built in from the start.',
                                                    'options': {   'A': 'It is a tool for designing secure systems — '
                                                                        'juice Shop is a deliberately insecure '
                                                                        'application for learning, not a design tool',
                                                                   'B': 'It highlights real-world failures of secure '
                                                                        'design and demonstrates threats and '
                                                                        'vulnerabilities',
                                                                   'C': 'It is a patch management platform — juice '
                                                                        'Shop is not a patch management platform',
                                                                   'D': 'It is a vulnerability scanner — juice Shop is '
                                                                        'a vulnerable app, not a scanner'},
                                                    'question': 'How does OWASP Juice Shop relate to secure design '
                                                                'principles?',
                                                    'wrong_explanations': {   'A': 'Juice Shop is a deliberately '
                                                                                   'insecure application for learning, '
                                                                                   'not a design tool.',
                                                                              'C': 'Juice Shop is not a patch '
                                                                                   'management platform.',
                                                                              'D': 'Juice Shop is a vulnerable app, '
                                                                                   'not a scanner.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'If security is too difficult to use, users find '
                                                                   'workarounds (e.g., writing down complex '
                                                                   'passwords). Ease of use is necessary to make users '
                                                                   'behave securely — usability and security are '
                                                                   'complementary, not opposing.',
                                                    'options': {   'A': 'Because users prefer fast systems over secure '
                                                                        'ones — the relationship between speed and '
                                                                        'security is nuanced — this is an '
                                                                        'oversimplification',
                                                                   'B': 'Because ease of use is necessary to make '
                                                                        'users behave securely — insecure workarounds '
                                                                        'emerge when security is too difficult',
                                                                   'C': 'Because security controls always reduce '
                                                                        "performance — security controls don't always "
                                                                        'reduce performance significantly',
                                                                   'D': 'Because GDPR requires usability testing — '
                                                                        'gDPR does not specifically require usability '
                                                                        'testing of security controls'},
                                                    'question': 'Why must security design NOT affect usability?',
                                                    'wrong_explanations': {   'A': 'The relationship between speed and '
                                                                                   'security is nuanced — this is an '
                                                                                   'oversimplification.',
                                                                              'C': "Security controls don't always "
                                                                                   'reduce performance significantly.',
                                                                              'D': 'GDPR does not specifically require '
                                                                                   'usability testing of security '
                                                                                   'controls.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Least Privilege means users, applications, and '
                                                                   'processes should have the minimum permissions '
                                                                   'required to do their job — reducing the attack '
                                                                   'surface and limiting damage if an account is '
                                                                   'compromised.',
                                                    'options': {   'A': 'Granting all users admin rights by default to '
                                                                        'improve productivity',
                                                                   'B': 'Granting users only the minimum access they '
                                                                        'need to perform their job function',
                                                                   'C': 'Restricting access to only the CEO and senior '
                                                                        'management — restriction to senior staff is '
                                                                        'not what least privilege means — it applies '
                                                                        'at every level',
                                                                   'D': 'Using the least expensive security tools — '
                                                                        'least privilege relates to access rights, not '
                                                                        'cost'},
                                                    'question': "What is the 'Principle of Least Privilege'?",
                                                    'wrong_explanations': {   'A': 'Admin rights for all users '
                                                                                   'massively increases risk — this is '
                                                                                   'the opposite of least privilege.',
                                                                              'C': 'Restriction to senior staff is not '
                                                                                   'what least privilege means — it '
                                                                                   'applies at every level.',
                                                                              'D': 'Least privilege relates to access '
                                                                                   'rights, not cost.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Attack Surface Reduction means disabling or '
                                                                   'removing unnecessary features, services, ports, '
                                                                   'and protocols — fewer entry points mean fewer '
                                                                   'opportunities for attackers.',
                                                    'options': {   'A': 'Adding more security tools to a system — '
                                                                        "adding tools doesn't reduce the attack "
                                                                        'surface — it may increase it',
                                                                   'B': 'Minimising the number of entry points an '
                                                                        'attacker can use — disabling unused services, '
                                                                        'ports, and features',
                                                                   'C': 'Using a Web Application Firewall — a WAF is a '
                                                                        'protective control, not attack surface '
                                                                        'reduction',
                                                                   'D': 'Encrypting all data at rest — encryption '
                                                                        "protects data confidentiality but doesn't "
                                                                        'reduce attack surface'},
                                                    'question': "What is 'Attack Surface Reduction' as a secure design "
                                                                'technique?',
                                                    'wrong_explanations': {   'A': "Adding tools doesn't reduce the "
                                                                                   'attack surface — it may increase '
                                                                                   'it.',
                                                                              'C': 'A WAF is a protective control, not '
                                                                                   'attack surface reduction.',
                                                                              'D': 'Encryption protects data '
                                                                                   "confidentiality but doesn't reduce "
                                                                                   'attack surface.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Security by Default means products are delivered '
                                                                   'in the most secure configuration. Users must '
                                                                   'actively choose to reduce security (e.g., enable '
                                                                   'unnecessary features), rather than actively '
                                                                   'enabling protections.',
                                                    'options': {   'A': 'Using default vendor passwords for all '
                                                                        'systems — default passwords are a security '
                                                                        'risk — Security by Default requires changing '
                                                                        'them',
                                                                   'B': 'Systems are shipped and configured in the '
                                                                        'most secure state out of the box, requiring '
                                                                        'action to reduce security',
                                                                   'C': 'Security policies apply only to default user '
                                                                        'accounts — security by Default applies to all '
                                                                        'users and configurations, not just default '
                                                                        'accounts',
                                                                   'D': 'Enabling all features by default to ensure '
                                                                        'nothing is missed — enabling all features '
                                                                        'increases the attack surface — this '
                                                                        'contradicts Security by Default'},
                                                    'question': "What is 'Security by Default'?",
                                                    'wrong_explanations': {   'A': 'Default passwords are a security '
                                                                                   'risk — Security by Default '
                                                                                   'requires changing them.',
                                                                              'C': 'Security by Default applies to all '
                                                                                   'users and configurations, not just '
                                                                                   'default accounts.',
                                                                              'D': 'Enabling all features increases '
                                                                                   'the attack surface — this '
                                                                                   'contradicts Security by Default.'}},
                                                {   'correct': 'C',
                                                    'explanation': "'Establish Context' is the first NCSC principle — "
                                                                   'you must understand the threat environment, '
                                                                   'assets, and business requirements before designing '
                                                                   'appropriate security measures.',
                                                    'options': {   'A': 'Make compromise difficult',
                                                                   'B': 'Make disruption difficult',
                                                                   'C': 'Establish context',
                                                                   'D': 'Reduce the impact of compromise'},
                                                    'question': 'Which NCSC principle involves understanding what you '
                                                                'are trying to protect before designing security?',
                                                    'wrong_explanations': {   'A': "'Make compromise difficult' is "
                                                                                   'about reducing attack surface and '
                                                                                   'validating inputs — the second '
                                                                                   'principle.',
                                                                              'B': "'Make disruption difficult' is "
                                                                                   'about availability and resilience '
                                                                                   '— the third principle.',
                                                                              'D': "'Reduce the impact of compromise' "
                                                                                   'focuses on limiting damage — the '
                                                                                   'fifth principle.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Threat modelling (e.g., using STRIDE) is done '
                                                                   'during design: identify assets, identify threats '
                                                                   'to each asset, assess risk, design mitigations. '
                                                                   'Far cheaper to fix security at design time than '
                                                                   'post-deployment.',
                                                    'options': {   'A': 'Creating a 3D model of security '
                                                                        'infrastructure — 3D infrastructure models are '
                                                                        'for visualisation — not security threat '
                                                                        'modelling',
                                                                   'B': 'A structured process for identifying, '
                                                                        'prioritising, and mitigating potential '
                                                                        'threats to a system during design — before '
                                                                        'building it',
                                                                   'C': 'Modelling attacker behaviour using machine '
                                                                        'learning — mL-based threat detection is '
                                                                        'anomaly detection — threat modelling is a '
                                                                        'manual design-time exercise',
                                                                   'D': 'A method for calculating risk scores — risk '
                                                                        'scoring is one output of threat modelling, '
                                                                        'not the process itself'},
                                                    'question': 'What is threat modelling?',
                                                    'wrong_explanations': {   'A': '3D infrastructure models are for '
                                                                                   'visualisation — not security '
                                                                                   'threat modelling.',
                                                                              'C': 'ML-based threat detection is '
                                                                                   'anomaly detection — threat '
                                                                                   'modelling is a manual design-time '
                                                                                   'exercise.',
                                                                              'D': 'Risk scoring is one output of '
                                                                                   'threat modelling, not the process '
                                                                                   'itself.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'STRIDE (Microsoft): Spoofing identity, Tampering '
                                                                   'with data, Repudiation, Information Disclosure, '
                                                                   'Denial of Service, Elevation of Privilege. Each '
                                                                   'threat maps to a violated security property (e.g., '
                                                                   'DoS → Availability).',
                                                    'options': {   'A': 'Scan, Test, Remediate, Identify, Deploy, '
                                                                        'Evaluate — scan/Test/Remediate is a security '
                                                                        'testing workflow — not the STRIDE acronym',
                                                                   'B': 'Spoofing, Tampering, Repudiation, Information '
                                                                        'Disclosure, Denial of Service, Elevation of '
                                                                        'Privilege',
                                                                   'C': 'Security, Threat, Risk, Impact, Detection, '
                                                                        'Exploitation — these are general security '
                                                                        'concepts — not what STRIDE stands for',
                                                                   'D': 'System, Threat, Response, Intelligence, '
                                                                        'Detection, Evaluation — these are not the '
                                                                        'STRIDE threat categories'},
                                                    'question': 'What does STRIDE stand for in threat modelling?',
                                                    'wrong_explanations': {   'A': 'Scan/Test/Remediate is a security '
                                                                                   'testing workflow — not the STRIDE '
                                                                                   'acronym.',
                                                                              'C': 'These are general security '
                                                                                   'concepts — not what STRIDE stands '
                                                                                   'for.',
                                                                              'D': 'These are not the STRIDE threat '
                                                                                   'categories.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Separation of Duties (SoD) ensures no single '
                                                                   'person can complete a sensitive process alone — '
                                                                   'e.g., a person who requests a payment cannot also '
                                                                   'approve it. Prevents insider fraud and reduces '
                                                                   'error risk.',
                                                    'options': {   'A': 'IT and security teams must work in separate '
                                                                        'buildings — physical separation of teams is '
                                                                        'not what SoD means',
                                                                   'B': 'Requiring more than one person to complete '
                                                                        'sensitive or high-risk tasks — preventing '
                                                                        'fraud, errors, and abuse of privilege',
                                                                   'C': 'Separating development and production '
                                                                        'environments — dev/prod environment '
                                                                        'separation is a change management/security '
                                                                        'control — related but not SoD',
                                                                   'D': 'Different staff managing different types of '
                                                                        'data — data-type segregation is a data '
                                                                        'management practice — SoD is about task '
                                                                        'completion requiring multiple people'},
                                                    'question': "What is the 'Principle of Separation of Duties'?",
                                                    'wrong_explanations': {   'A': 'Physical separation of teams is '
                                                                                   'not what SoD means.',
                                                                              'C': 'Dev/prod environment separation is '
                                                                                   'a change management/security '
                                                                                   'control — related but not SoD.',
                                                                              'D': 'Data-type segregation is a data '
                                                                                   'management practice — SoD is about '
                                                                                   'task completion requiring multiple '
                                                                                   'people.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Fail-safe defaults (Saltzer & Schroeder): the '
                                                                   "default is 'deny'. If an access control mechanism "
                                                                   "fails or a case isn't explicitly covered, access "
                                                                   'is denied — not granted. Prevents gaps in access '
                                                                   'control coverage.',
                                                    'options': {   'A': 'Systems that fail without causing data '
                                                                        'corruption — data corruption prevention is '
                                                                        'about data integrity controls — not fail-safe '
                                                                        'defaults',
                                                                   'B': 'Access decisions default to denial — users '
                                                                        'must be explicitly granted access; access is '
                                                                        'not allowed unless specifically authorised',
                                                                   'C': 'Systems that automatically restart after '
                                                                        'failure — automatic restart on failure is '
                                                                        'about availability — fail-safe defaults are '
                                                                        'about access control',
                                                                   'D': 'Default passwords that are difficult to crack '
                                                                        '— default password strength is a separate '
                                                                        'security concern'},
                                                    'question': "What is 'fail-safe defaults' as a design principle?",
                                                    'wrong_explanations': {   'A': 'Data corruption prevention is '
                                                                                   'about data integrity controls — '
                                                                                   'not fail-safe defaults.',
                                                                              'C': 'Automatic restart on failure is '
                                                                                   'about availability — fail-safe '
                                                                                   'defaults are about access control.',
                                                                              'D': 'Default password strength is a '
                                                                                   'separate security concern.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Economy of mechanism (Saltzer & Schroeder): simple '
                                                                   'security mechanisms are easier to verify, test, '
                                                                   'and maintain. Complexity is the enemy of security '
                                                                   "— 'security through complexity' often fails.",
                                                    'options': {   'A': 'Using the cheapest security tools available — '
                                                                        'cost minimisation is not the principle — '
                                                                        'simplicity is',
                                                                   'B': 'Keeping security mechanisms as simple as '
                                                                        'possible — complex designs have more '
                                                                        'potential for bugs and misconfigurations',
                                                                   'C': 'Minimising the economic impact of security '
                                                                        'incidents — economic impact of incidents is a '
                                                                        'risk management concern, not this principle',
                                                                   'D': 'Using efficient algorithms to reduce '
                                                                        'computational overhead — algorithmic '
                                                                        'efficiency is a performance concern — not '
                                                                        'economy of mechanism'},
                                                    'question': "What is 'economy of mechanism' as a design principle?",
                                                    'wrong_explanations': {   'A': 'Cost minimisation is not the '
                                                                                   'principle — simplicity is.',
                                                                              'C': 'Economic impact of incidents is a '
                                                                                   'risk management concern, not this '
                                                                                   'principle.',
                                                                              'D': 'Algorithmic efficiency is a '
                                                                                   'performance concern — not economy '
                                                                                   'of mechanism.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Complete mediation means every access attempt is '
                                                                   'authorised — no shortcuts or caching that could be '
                                                                   'exploited. If a permission is revoked, the next '
                                                                   'access check should enforce the revocation '
                                                                   'immediately.',
                                                    'options': {   'A': 'Using a mediator (trusted third party) for '
                                                                        'all transactions — trusted third-party '
                                                                        'mediation is a different concept — complete '
                                                                        'mediation is about consistent access checking',
                                                                   'B': 'Every access to every resource must be '
                                                                        'checked against the access control system — '
                                                                        'caching access decisions is dangerous',
                                                                   'C': 'All communications must go through a central '
                                                                        'gateway — central gateways are one '
                                                                        'implementation — complete mediation is the '
                                                                        'principle of always checking',
                                                                   'D': 'Complete documentation of all security '
                                                                        'decisions — documentation is important but '
                                                                        'not what complete mediation means'},
                                                    'question': "What is the 'complete mediation' security design "
                                                                'principle?',
                                                    'wrong_explanations': {   'A': 'Trusted third-party mediation is a '
                                                                                   'different concept — complete '
                                                                                   'mediation is about consistent '
                                                                                   'access checking.',
                                                                              'C': 'Central gateways are one '
                                                                                   'implementation — complete '
                                                                                   'mediation is the principle of '
                                                                                   'always checking.',
                                                                              'D': 'Documentation is important but not '
                                                                                   'what complete mediation means.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Psychological acceptability (Saltzer & Schroeder): '
                                                                   "security shouldn't be so burdensome that users "
                                                                   'circumvent it. If a mechanism is too hard to use '
                                                                   'correctly, users will find insecure workarounds — '
                                                                   'e.g., writing down overly complex passwords.',
                                                    'options': {   'A': 'Making security tools that users find '
                                                                        'aesthetically pleasing — aesthetics are '
                                                                        'irrelevant — usability and correct use are '
                                                                        'the concern',
                                                                   'B': 'Security mechanisms should not make the '
                                                                        'resource harder to access than if the '
                                                                        'protection were not present — users must be '
                                                                        'able to use them correctly',
                                                                   'C': 'Ensuring users psychologically accept '
                                                                        'security training — accepting training is a '
                                                                        'behaviour — psychological acceptability is '
                                                                        'about mechanism design',
                                                                   'D': 'Making security decisions based on user '
                                                                        'preferences — security decisions should be '
                                                                        'based on risk, not user preferences'},
                                                    'question': "What is 'psychological acceptability' as a security "
                                                                'design principle?',
                                                    'wrong_explanations': {   'A': 'Aesthetics are irrelevant — '
                                                                                   'usability and correct use are the '
                                                                                   'concern.',
                                                                              'C': 'Accepting training is a behaviour '
                                                                                   '— psychological acceptability is '
                                                                                   'about mechanism design.',
                                                                              'D': 'Security decisions should be based '
                                                                                   'on risk, not user preferences.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'The SDLC covers all phases of software creation. '
                                                                   'Security integrated at each phase (Secure SDLC) is '
                                                                   'far cheaper than fixing vulnerabilities '
                                                                   'post-release — cost of fixing bugs increases '
                                                                   'dramatically through the lifecycle.',
                                                    'options': {   'A': 'A lifecycle for replacing outdated software — '
                                                                        'software replacement is an asset management '
                                                                        'concern — not the SDLC',
                                                                   'B': 'The process of planning, designing, building, '
                                                                        'testing, deploying, and maintaining software '
                                                                        '— security must be integrated at each stage '
                                                                        'to prevent vulnerabilities',
                                                                   'C': 'A lifecycle for software licensing management '
                                                                        '— licensing management is an IT asset '
                                                                        'management function',
                                                                   'D': 'An agile development methodology — agile is a '
                                                                        'specific development methodology — the SDLC '
                                                                        'encompasses multiple methodologies'},
                                                    'question': "What is a 'Software Development Lifecycle' (SDLC) and "
                                                                'why does security need to be integrated into it?',
                                                    'wrong_explanations': {   'A': 'Software replacement is an asset '
                                                                                   'management concern — not the SDLC.',
                                                                              'C': 'Licensing management is an IT '
                                                                                   'asset management function.',
                                                                              'D': 'Agile is a specific development '
                                                                                   'methodology — the SDLC encompasses '
                                                                                   'multiple methodologies.'}},
                                                {   'correct': 'B',
                                                    'explanation': "Open design (Kerckhoffs's Principle): security "
                                                                   'mechanisms should be secure even if everything '
                                                                   "except the key is public knowledge. 'Security "
                                                                   "through obscurity' — relying on secret algorithms "
                                                                   '— is not reliable security.',
                                                    'options': {   'A': 'Making all source code publicly available — '
                                                                        'open source is a software licensing concept — '
                                                                        'open design is a security principle about not '
                                                                        'relying on algorithmic secrecy',
                                                                   'B': 'Security of a system should not depend on '
                                                                        'secrecy of its design — assume attackers know '
                                                                        'the algorithm; security comes from '
                                                                        'key/credential secrecy',
                                                                   'C': 'Designing open-source security tools — '
                                                                        'open-source security tools are an '
                                                                        'implementation choice — not the open design '
                                                                        'principle',
                                                                   'D': 'Using publicly audited security standards — '
                                                                        'using public standards is good practice but '
                                                                        'not the definition of open design'},
                                                    'question': "What is 'open design' as a security principle?",
                                                    'wrong_explanations': {   'A': 'Open source is a software '
                                                                                   'licensing concept — open design is '
                                                                                   'a security principle about not '
                                                                                   'relying on algorithmic secrecy.',
                                                                              'C': 'Open-source security tools are an '
                                                                                   'implementation choice — not the '
                                                                                   'open design principle.',
                                                                              'D': 'Using public standards is good '
                                                                                   'practice but not the definition of '
                                                                                   'open design.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Vulnerability scanning identifies what might be '
                                                                   'exploitable (automated). Penetration testing '
                                                                   'actively exploits vulnerabilities to demonstrate '
                                                                   'real impact — shows what an attacker could '
                                                                   'actually achieve, not just what might be '
                                                                   'vulnerable.',
                                                    'options': {   'A': 'They are the same thing — they serve '
                                                                        'different purposes and produce different '
                                                                        'depths of findings',
                                                                   'B': 'A penetration test has a human tester '
                                                                        'actively attempting to exploit '
                                                                        'vulnerabilities (simulate a real attack); a '
                                                                        'vulnerability scan only identifies potential '
                                                                        'vulnerabilities automatically',
                                                                   'C': 'A penetration test only tests external '
                                                                        'systems; a vulnerability scan tests internal '
                                                                        'systems — both can test internal and external '
                                                                        'systems',
                                                                   'D': 'A penetration test uses automated tools; a '
                                                                        'vulnerability scan uses manual techniques — '
                                                                        'this is backwards — penetration tests use '
                                                                        'human expertise; vulnerability scans are '
                                                                        'automated'},
                                                    'question': "What is a 'penetration test' and how does it differ "
                                                                'from a vulnerability scan?',
                                                    'wrong_explanations': {   'A': 'They serve different purposes and '
                                                                                   'produce different depths of '
                                                                                   'findings.',
                                                                              'C': 'Both can test internal and '
                                                                                   'external systems.',
                                                                              'D': 'This is backwards — penetration '
                                                                                   'tests use human expertise; '
                                                                                   'vulnerability scans are '
                                                                                   'automated.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Network segmentation (firewalls, VLANs, DMZ) '
                                                                   'limits lateral movement — if one zone is '
                                                                   'compromised, the attacker faces additional '
                                                                   'barriers reaching the next zone. Critical systems '
                                                                   '(e.g., payment servers) are in isolated segments.',
                                                    'options': {   'A': 'Dividing the network into VLANs to improve '
                                                                        'performance only — vLANs improve performance '
                                                                        "too, but segmentation's security purpose is "
                                                                        'breach containment',
                                                                   'B': 'Dividing a network into isolated zones — '
                                                                        'limiting the blast radius of a breach, so '
                                                                        'attackers who compromise one segment cannot '
                                                                        'easily reach others',
                                                                   'C': 'Segmenting the internet connection for '
                                                                        'different departments — segmenting internet '
                                                                        'connections is bandwidth management — network '
                                                                        'segmentation is about access boundaries',
                                                                   'D': 'Physically separating servers by function — '
                                                                        'physical separation is one form — logical '
                                                                        'segmentation using firewalls/VLANs is more '
                                                                        'common'},
                                                    'question': "What is 'network segmentation' and why is it a secure "
                                                                'design technique?',
                                                    'wrong_explanations': {   'A': 'VLANs improve performance too, but '
                                                                                   "segmentation's security purpose is "
                                                                                   'breach containment.',
                                                                              'C': 'Segmenting internet connections is '
                                                                                   'bandwidth management — network '
                                                                                   'segmentation is about access '
                                                                                   'boundaries.',
                                                                              'D': 'Physical separation is one form — '
                                                                                   'logical segmentation using '
                                                                                   'firewalls/VLANs is more common.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'A DMZ sits between two firewalls — public servers '
                                                                   '(web, mail) face the internet in the DMZ. Even if '
                                                                   'compromised, attackers cannot directly reach the '
                                                                   'internal network. The second firewall protects '
                                                                   'internal systems.',
                                                    'options': {   'A': 'A physical zone where no weapons are allowed, '
                                                                        'repurposed for IT — the term is borrowed from '
                                                                        'military but the IT concept is about network '
                                                                        'isolation',
                                                                   'B': 'A network segment between the internet and '
                                                                        'internal network — hosting public-facing '
                                                                        'servers (web, email) while isolating the '
                                                                        'internal network',
                                                                   'C': 'A firewall rule that demilitarises all '
                                                                        'traffic — a DMZ is a network zone, not a '
                                                                        'firewall rule',
                                                                   'D': 'A network zone with no security controls for '
                                                                        'testing — a DMZ has security controls — it is '
                                                                        'carefully controlled, not uncontrolled'},
                                                    'question': "What is a 'DMZ' (Demilitarised Zone) in network "
                                                                'architecture?',
                                                    'wrong_explanations': {   'A': 'The term is borrowed from military '
                                                                                   'but the IT concept is about '
                                                                                   'network isolation.',
                                                                              'C': 'A DMZ is a network zone, not a '
                                                                                   'firewall rule.',
                                                                              'D': 'A DMZ has security controls — it '
                                                                                   'is carefully controlled, not '
                                                                                   'uncontrolled.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Zero Trust assumes compromise is possible from any '
                                                                   'location — internal users are not automatically '
                                                                   'trusted. Every request is verified (identity, '
                                                                   'device health, context), and least privilege is '
                                                                   'enforced continuously.',
                                                    'options': {   'A': 'An architecture where all traffic is blocked '
                                                                        'by default — blocking all traffic would '
                                                                        'prevent operations — Zero Trust verifies '
                                                                        'traffic, not blocks it all',
                                                                   'B': 'Never trust, always verify — no implicit '
                                                                        'trust based on network location; every access '
                                                                        'request is authenticated and authorised '
                                                                        'regardless of origin',
                                                                   'C': 'A network design with zero single points of '
                                                                        'failure — high availability design (no single '
                                                                        'points of failure) is about resilience, not '
                                                                        'Zero Trust',
                                                                   'D': 'A security model that trusts only hardware '
                                                                        'components — hardware-only trust is a concept '
                                                                        'in hardware security — not Zero Trust '
                                                                        'Architecture'},
                                                    'question': "What is 'Zero Trust Architecture' and what is its "
                                                                'core principle?',
                                                    'wrong_explanations': {   'A': 'Blocking all traffic would prevent '
                                                                                   'operations — Zero Trust verifies '
                                                                                   'traffic, not blocks it all.',
                                                                              'C': 'High availability design (no '
                                                                                   'single points of failure) is about '
                                                                                   'resilience, not Zero Trust.',
                                                                              'D': 'Hardware-only trust is a concept '
                                                                                   'in hardware security — not Zero '
                                                                                   'Trust Architecture.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Threat intelligence sharing (via ISACs, '
                                                                   'STIX/TAXII, FS-ISAC) allows organisations to share '
                                                                   'IoCs, attacker tools, and techniques — one '
                                                                   "organisation's detected attack becomes early "
                                                                   'warning for others.',
                                                    'options': {   'A': 'Sharing vulnerability scanner results between '
                                                                        'departments — scanner results sharing is '
                                                                        'useful but not what threat intelligence '
                                                                        'sharing formally means',
                                                                   'B': 'Organisations sharing information about '
                                                                        'current threats, indicators of compromise, '
                                                                        'and attacker TTPs — enabling the community to '
                                                                        'defend against threats faster',
                                                                   'C': 'Sharing threat models with software vendors — '
                                                                        'sharing with vendors is vendor collaboration '
                                                                        '— threat intel sharing is broader community '
                                                                        'sharing',
                                                                   'D': 'Government intelligence agencies sharing '
                                                                        'cyber data publicly — government agencies '
                                                                        'participate but threat intel sharing is '
                                                                        'predominantly industry-led'},
                                                    'question': "What is 'threat intelligence sharing' and why is it "
                                                                'valuable?',
                                                    'wrong_explanations': {   'A': 'Scanner results sharing is useful '
                                                                                   'but not what threat intelligence '
                                                                                   'sharing formally means.',
                                                                              'C': 'Sharing with vendors is vendor '
                                                                                   'collaboration — threat intel '
                                                                                   'sharing is broader community '
                                                                                   'sharing.',
                                                                              'D': 'Government agencies participate '
                                                                                   'but threat intel sharing is '
                                                                                   'predominantly industry-led.'}},
                                                {   'correct': 'B',
                                                    'explanation': 'Security code reviews examine source code for '
                                                                   'vulnerabilities — hardcoded credentials, SQL '
                                                                   'injection risks, insecure cryptography, missing '
                                                                   'authentication. Fixing at code review stage is far '
                                                                   'cheaper than post-deployment.',
                                                    'options': {   'A': 'To check code style and formatting — code '
                                                                        'style is checked by linters — security review '
                                                                        'focuses on security vulnerabilities',
                                                                   'B': 'To identify security vulnerabilities in code '
                                                                        'before deployment — spotting injection flaws, '
                                                                        'insecure configurations, hardcoded '
                                                                        'credentials, and logic errors',
                                                                   'C': 'To verify that the application meets '
                                                                        'functional requirements — functional testing '
                                                                        'verifies features work — security review '
                                                                        'finds security flaws',
                                                                   'D': 'To test application performance under load — '
                                                                        'load testing is performance engineering — not '
                                                                        'security review'},
                                                    'question': "What is the purpose of a 'security review' or 'code "
                                                                "review' in the SDLC?",
                                                    'wrong_explanations': {   'A': 'Code style is checked by linters — '
                                                                                   'security review focuses on '
                                                                                   'security vulnerabilities.',
                                                                              'C': 'Functional testing verifies '
                                                                                   'features work — security review '
                                                                                   'finds security flaws.',
                                                                              'D': 'Load testing is performance '
                                                                                   'engineering — not security '
                                                                                   'review.'}}],
    'Week 9 - Vulnerability Scanning': [   {   'correct': 'B',
                                               'explanation': 'Vulnerability scanning is a proactive process of '
                                                              'systematically identifying, assessing, and reporting '
                                                              'security vulnerabilities in systems, networks, and '
                                                              'applications before attackers can exploit them.',
                                               'options': {   'A': 'Actively exploiting vulnerabilities to gain access '
                                                                   '— actively exploiting vulnerabilities is '
                                                                   'penetration testing',
                                                              'B': 'Systematically identifying, assessing, and '
                                                                   'reporting security weaknesses',
                                                              'C': 'Monitoring network traffic for suspicious activity '
                                                                   '— real-time traffic monitoring is an IDS function',
                                                              'D': 'Encrypting sensitive data — encryption is a '
                                                                   'security control, not a scanning technique'},
                                               'question': 'What is vulnerability scanning?',
                                               'wrong_explanations': {   'A': 'Actively exploiting vulnerabilities is '
                                                                              'penetration testing.',
                                                                         'C': 'Real-time traffic monitoring is an IDS '
                                                                              'function.',
                                                                         'D': 'Encryption is a security control, not a '
                                                                              'scanning technique.'}},
                                           {   'correct': 'C',
                                               'explanation': 'The four types are: Network Vulnerability Scanning, Web '
                                                              'Application Vulnerability Scanning, Host-based '
                                                              'Scanning, and Database Scanning. Bluetooth scanning is '
                                                              'not listed.',
                                               'options': {   'A': 'Network Vulnerability Scanning',
                                                              'B': 'Web Application Scanning',
                                                              'C': 'Bluetooth Scanning',
                                                              'D': 'Host-based Scanning'},
                                               'question': 'Which is NOT one of the four types of vulnerability '
                                                           'scanning from the lecture?',
                                               'wrong_explanations': {   'A': 'Network Vulnerability Scanning is one '
                                                                              'of the four types.',
                                                                         'B': 'Web Application Scanning is one of the '
                                                                              'four types.',
                                                                         'D': 'Host-based Scanning is one of the four '
                                                                              'types.'}},
                                           {   'correct': 'C',
                                               'explanation': 'Nessus Essentials v10.11.3 was used for automated '
                                                              'vulnerability scanning in Week 9 against the target '
                                                              'Ubuntu/WordPress VM.',
                                               'options': {   'A': 'WPScan',
                                                              'B': 'Metasploit',
                                                              'C': 'Nessus Essentials',
                                                              'D': 'Wireshark'},
                                               'question': 'What tool was used for automated vulnerability scanning in '
                                                           'the Week 9 lab?',
                                               'wrong_explanations': {   'A': 'WPScan was used in Week 5 for '
                                                                              'WordPress-specific scanning.',
                                                                         'B': 'Metasploit is an exploitation '
                                                                              'framework.',
                                                                         'D': 'Wireshark is a packet analyser, not a '
                                                                              'vulnerability scanner.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Patch Management involves regularly applying security '
                                                              'patches and updates. It is one of the most effective '
                                                              'mitigation strategies as it directly removes known '
                                                              'vulnerabilities.',
                                               'options': {   'A': 'Configuration Hardening',
                                                              'B': 'Patch Management',
                                                              'C': 'Access Control',
                                                              'D': 'Encryption'},
                                               'question': 'Which mitigation strategy involves applying software '
                                                           'updates to fix known vulnerabilities?',
                                               'wrong_explanations': {   'A': 'Configuration Hardening involves '
                                                                              'securely configuring systems (disabling '
                                                                              'unnecessary services, changing '
                                                                              'defaults).',
                                                                         'C': 'Access Control restricts who can access '
                                                                              'systems/data.',
                                                                         'D': 'Encryption protects data '
                                                                              'confidentiality.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Correct order: Asset Identification → Threat Evaluation '
                                                              '→ Vulnerability Appraisal → Risk Assessment → Risk '
                                                              'Mitigation. You must know your assets before evaluating '
                                                              'threats against them.',
                                               'options': {   'A': 'Threat Evaluation → Asset Identification → '
                                                                   'Vulnerability Appraisal → Risk Assessment → Risk '
                                                                   'Mitigation',
                                                              'B': 'Asset Identification → Threat Evaluation → '
                                                                   'Vulnerability Appraisal → Risk Assessment → Risk '
                                                                   'Mitigation',
                                                              'C': 'Vulnerability Appraisal → Asset Identification → '
                                                                   'Threat Evaluation → Risk Mitigation → Risk '
                                                                   'Assessment',
                                                              'D': 'Risk Assessment → Asset Identification → Threat '
                                                                   'Evaluation → Vulnerability Appraisal → Risk '
                                                                   'Mitigation'},
                                               'question': 'What are the five steps of the Vulnerability Assessment '
                                                           'process in the correct order?',
                                               'wrong_explanations': {   'A': 'You must identify assets before '
                                                                              'evaluating threats.',
                                                                         'C': 'You cannot appraise vulnerabilities '
                                                                              'before identifying assets.',
                                                                         'D': 'Risk Assessment comes after identifying '
                                                                              'assets, threats, and vulnerabilities.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Honeypots are decoy systems set up to attract '
                                                              'attackers. When attackers interact with them, defenders '
                                                              'gather intelligence on attack techniques, tools, and '
                                                              'methods. Honeynets are networks of honeypots.',
                                               'options': {   'A': 'Storing encrypted passwords — password storage is '
                                                                   'a database/authentication function',
                                                              'B': 'A decoy system designed to lure attackers and '
                                                                   'gather intelligence on attack methods',
                                                              'C': 'Scanning networks for open ports — port scanning '
                                                                   'is done by tools like Nmap',
                                                              'D': 'Automatically patching vulnerabilities — automatic '
                                                                   'patching is done by patch management systems'},
                                               'question': 'What is a Honeypot used for in vulnerability assessment?',
                                               'wrong_explanations': {   'A': 'Password storage is a '
                                                                              'database/authentication function.',
                                                                         'C': 'Port scanning is done by tools like '
                                                                              'Nmap.',
                                                                         'D': 'Automatic patching is done by patch '
                                                                              'management systems.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Common detected vulnerabilities include: unpatched '
                                                              'systems, server misconfigurations, web application '
                                                              'vulnerabilities, weak/default credentials, insecure '
                                                              'communication protocols, and open/unnecessary ports.',
                                               'options': {   'A': 'Outdated browser extensions',
                                                              'B': 'Weak passwords or default credentials',
                                                              'C': 'Slow network speeds',
                                                              'D': 'Unlicensed software'},
                                               'question': "Which of the following is listed as a 'common detected "
                                                           "vulnerability' in the Week 9 lecture?",
                                               'wrong_explanations': {   'A': 'Browser extensions are not listed as a '
                                                                              'common detected vulnerability.',
                                                                         'C': 'Network speed is a performance issue, '
                                                                              'not a security vulnerability.',
                                                                         'D': 'Unlicensed software is a '
                                                                              'legal/compliance issue, not a '
                                                                              'vulnerability type in this context.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Configuration Hardening involves securely configuring '
                                                              'systems — disabling unnecessary services, removing '
                                                              'default accounts/passwords, closing unused ports, and '
                                                              'minimising the attack surface.',
                                               'options': {   'A': 'Applying software patches to fix known bugs — '
                                                                   'applying patches is Patch Management',
                                                              'B': 'Securely configuring systems by disabling '
                                                                   'unnecessary services and changing default settings',
                                                              'C': 'Encrypting all data at rest and in transit — '
                                                                   'encrypting data is the Encryption mitigation '
                                                                   'strategy',
                                                              'D': 'Installing antivirus software on all endpoints — '
                                                                   "installing antivirus falls under 'Use of Security "
                                                                   "Tools'"},
                                               'question': "What is 'Configuration Hardening' as a mitigation "
                                                           'strategy?',
                                               'wrong_explanations': {   'A': 'Applying patches is Patch Management.',
                                                                         'C': 'Encrypting data is the Encryption '
                                                                              'mitigation strategy.',
                                                                         'D': "Installing antivirus falls under 'Use "
                                                                              "of Security Tools'."}},
                                           {   'correct': 'B',
                                               'explanation': 'Many regulations like PCI-DSS (payment cards), GDPR '
                                                              '(data protection), and HIPAA (healthcare) require '
                                                              'organisations to regularly identify and remediate '
                                                              'vulnerabilities as part of compliance.',
                                               'options': {   'A': 'Governments require all organisations to scan '
                                                                   'daily — daily scanning is not universally mandated '
                                                                   'by governments',
                                                              'B': 'Many regulations (PCI-DSS, GDPR, HIPAA) require '
                                                                   'organisations to regularly assess and address '
                                                                   'vulnerabilities',
                                                              'C': 'Scanning automatically makes organisations '
                                                                   'compliant — scanning identifies vulnerabilities '
                                                                   'but remediation is also required for compliance',
                                                              'D': 'It reduces insurance premiums automatically — '
                                                                   'while scanning may help with insurance '
                                                                   "assessments, it doesn't automatically reduce "
                                                                   'premiums'},
                                               'question': "Why is 'Regulatory Compliance' listed as an importance of "
                                                           'vulnerability scanning?',
                                               'wrong_explanations': {   'A': 'Daily scanning is not universally '
                                                                              'mandated by governments.',
                                                                         'C': 'Scanning identifies vulnerabilities but '
                                                                              'remediation is also required for '
                                                                              'compliance.',
                                                                         'D': 'While scanning may help with insurance '
                                                                              "assessments, it doesn't automatically "
                                                                              'reduce premiums.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Protocol analysers (like Wireshark) capture and analyse '
                                                              'network traffic to identify insecure protocols, '
                                                              'unencrypted data, and communication-level '
                                                              'vulnerabilities.',
                                               'options': {   'A': 'A tool that automatically patches vulnerabilities '
                                                                   '— auto-patching is a patch management function',
                                                              'B': 'A tool that captures and analyses network traffic '
                                                                   'to identify security weaknesses in communications',
                                                              'C': 'A policy framework for assessing risks — policy '
                                                                   'frameworks are not protocol analysers',
                                                              'D': 'A scanner that identifies outdated software '
                                                                   'versions — identifying outdated software versions '
                                                                   'is done by vulnerability scanners like Nessus'},
                                               'question': "What is a 'Protocol Analyser' as a vulnerability "
                                                           'assessment technique?',
                                               'wrong_explanations': {   'A': 'Auto-patching is a patch management '
                                                                              'function.',
                                                                         'C': 'Policy frameworks are not protocol '
                                                                              'analysers.',
                                                                         'D': 'Identifying outdated software versions '
                                                                              'is done by vulnerability scanners like '
                                                                              'Nessus.'}},
                                           {   'correct': 'B',
                                               'explanation': 'CVE is a standardised dictionary of publicly known '
                                                              'security vulnerabilities. Each entry gets a unique ID '
                                                              '(e.g., CVE-2021-44228 for Log4Shell), enabling '
                                                              'consistent tracking and communication about '
                                                              'vulnerabilities.',
                                               'options': {   'A': 'A type of malware that exploits system weaknesses '
                                                                   '— cVE is a naming system, not a type of malware',
                                                              'B': 'A standardised identifier for publicly known '
                                                                   'security vulnerabilities',
                                                              'C': 'A tool used to scan for open ports — port scanning '
                                                                   'is done by tools like Nmap — CVE is a catalogue',
                                                              'D': 'A government-mandated security standard — cVE is '
                                                                   'maintained by MITRE, not a government mandate'},
                                               'question': 'What is a CVE (Common Vulnerabilities and Exposures)?',
                                               'wrong_explanations': {   'A': 'CVE is a naming system, not a type of '
                                                                              'malware.',
                                                                         'C': 'Port scanning is done by tools like '
                                                                              'Nmap — CVE is a catalogue.',
                                                                         'D': 'CVE is maintained by MITRE, not a '
                                                                              'government mandate.'}},
                                           {   'correct': 'B',
                                               'explanation': 'CVSS provides a standardised numerical score (0.0 to '
                                                              '10.0) for vulnerability severity: Low (0.1-3.9), Medium '
                                                              '(4.0-6.9), High (7.0-8.9), Critical (9.0-10.0). Helps '
                                                              'prioritise remediation.',
                                               'options': {   'A': 'A list of known vulnerabilities with unique IDs — '
                                                                   'the list of known vulnerabilities with IDs is the '
                                                                   'CVE database',
                                                              'B': 'A numerical scoring system (0-10) that rates the '
                                                                   'severity of security vulnerabilities',
                                                              'C': 'A tool for automatically patching vulnerabilities '
                                                                   '— auto-patching is a patch management function — '
                                                                   'CVSS just scores severity',
                                                              'D': 'A government database of reported cybercrime — '
                                                                   'cVSS is not a crime database — it scores technical '
                                                                   'vulnerability severity'},
                                               'question': 'What is the CVSS (Common Vulnerability Scoring System)?',
                                               'wrong_explanations': {   'A': 'The list of known vulnerabilities with '
                                                                              'IDs is the CVE database.',
                                                                         'C': 'Auto-patching is a patch management '
                                                                              'function — CVSS just scores severity.',
                                                                         'D': 'CVSS is not a crime database — it '
                                                                              'scores technical vulnerability '
                                                                              'severity.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Credentialed scans authenticate to the system (like a '
                                                              'logged-in user) and find internal vulnerabilities '
                                                              '(missing patches, misconfigurations). Non-credentialed '
                                                              "scans simulate an external attacker's view and find "
                                                              'fewer vulnerabilities.',
                                               'options': {   'A': 'There is no difference — both produce the same '
                                                                   'results — they produce significantly different '
                                                                   'results — credentialed scans find far more',
                                                              'B': 'A credentialed scan uses valid login credentials '
                                                                   'to access the system internally, finding more '
                                                                   'vulnerabilities; a non-credentialed scan only sees '
                                                                   'what an external attacker would see',
                                                              'C': 'A credentialed scan is illegal; non-credentialed '
                                                                   'is legal — both are legal when authorised — the '
                                                                   'legality depends on permission, not credential use',
                                                              'D': 'A credentialed scan only checks network ports; '
                                                                   'non-credentialed checks all services — this is '
                                                                   'backwards — non-credentialed scans are limited to '
                                                                   'external-facing interfaces'},
                                               'question': "What is the difference between a 'credentialed' and "
                                                           "'non-credentialed' vulnerability scan?",
                                               'wrong_explanations': {   'A': 'They produce significantly different '
                                                                              'results — credentialed scans find far '
                                                                              'more.',
                                                                         'C': 'Both are legal when authorised — the '
                                                                              'legality depends on permission, not '
                                                                              'credential use.',
                                                                         'D': 'This is backwards — non-credentialed '
                                                                              'scans are limited to external-facing '
                                                                              'interfaces.'}},
                                           {   'correct': 'B',
                                               'explanation': 'A false positive is when the scanner reports a '
                                                              'vulnerability that does not actually exist — it '
                                                              'requires manual verification. Too many false positives '
                                                              'waste time and erode trust in the scanner.',
                                               'options': {   'A': 'A real vulnerability that the scanner missed — a '
                                                                   "real vulnerability the scanner missed is a 'false "
                                                                   "negative' — more dangerous",
                                                              'B': 'A vulnerability that is reported by the scanner '
                                                                   'but does not actually exist on the system',
                                                              'C': 'A vulnerability with a CVSS score of 10 — a CVSS '
                                                                   'score of 10 is a Critical vulnerability — not a '
                                                                   'false positive',
                                                              'D': 'A scan that runs successfully without errors — a '
                                                                   'successful scan has nothing to do with false '
                                                                   'positives'},
                                               'question': "What is 'false positive' in the context of vulnerability "
                                                           'scanning?',
                                               'wrong_explanations': {   'A': 'A real vulnerability the scanner missed '
                                                                              "is a 'false negative' — more dangerous.",
                                                                         'C': 'A CVSS score of 10 is a Critical '
                                                                              'vulnerability — not a false positive.',
                                                                         'D': 'A successful scan has nothing to do '
                                                                              'with false positives.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Black box testing simulates an external attacker — no '
                                                              'knowledge of internal architecture, source code, or '
                                                              "credentials. It tests what's visible from outside, "
                                                              'reflecting a realistic attacker perspective.',
                                               'options': {   'A': 'Testing using a specialised black box hardware '
                                                                   "device — the 'box' is metaphorical — not hardware",
                                                              'B': 'The tester has no prior knowledge of the target '
                                                                   'system — simulating an external attacker with zero '
                                                                   'inside information',
                                                              'C': 'Testing only the backend/server components of an '
                                                                   'application — backend testing is not what black '
                                                                   'box means',
                                                              'D': 'Automated testing without human testers — black '
                                                                   'box can be manual or automated — the distinction '
                                                                   'is knowledge level'},
                                               'question': "What is 'black box' penetration testing?",
                                               'wrong_explanations': {   'A': "The 'box' is metaphorical — not "
                                                                              'hardware.',
                                                                         'C': 'Backend testing is not what black box '
                                                                              'means.',
                                                                         'D': 'Black box can be manual or automated — '
                                                                              'the distinction is knowledge level.'}},
                                           {   'correct': 'B',
                                               'explanation': 'White box (crystal/glass box) testing: tester has '
                                                              'complete knowledge. More thorough — can test internal '
                                                              'logic, check for hardcoded credentials, audit code. '
                                                              'More expensive but finds more vulnerabilities.',
                                               'options': {   'A': 'Testing in a white room or sterile environment — '
                                                                   "the environment colour is irrelevant — it's about "
                                                                   'information provided to the tester',
                                                              'B': 'The tester has full knowledge of the target — '
                                                                   'source code, architecture, credentials — enabling '
                                                                   'thorough testing of all components',
                                                              'C': 'Testing only the frontend user interface — '
                                                                   'frontend-only testing is not white box testing',
                                                              'D': 'Testing conducted by the internal security team — '
                                                                   'internal team testing can be black or white box — '
                                                                   'the key is knowledge level'},
                                               'question': "What is 'white box' penetration testing?",
                                               'wrong_explanations': {   'A': 'The environment colour is irrelevant — '
                                                                              "it's about information provided to the "
                                                                              'tester.',
                                                                         'C': 'Frontend-only testing is not white box '
                                                                              'testing.',
                                                                         'D': 'Internal team testing can be black or '
                                                                              'white box — the key is knowledge '
                                                                              'level.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Grey box testing gives testers some information (e.g., '
                                                              'login credentials, network diagrams) but not full '
                                                              'source code access — simulating an insider threat or '
                                                              'attacker who has obtained some credentials.',
                                               'options': {   'A': 'Testing conducted in low-light conditions — '
                                                                   'lighting conditions are irrelevant to penetration '
                                                                   'testing',
                                                              'B': 'The tester has partial knowledge — simulating an '
                                                                   'insider threat or authenticated user who knows '
                                                                   'some details but not everything',
                                                              'C': 'Testing that combines automated and manual '
                                                                   'techniques — combined automated/manual techniques '
                                                                   'describe a testing methodology, not grey box '
                                                                   'testing',
                                                              'D': 'Testing with restricted access to only some '
                                                                   'systems — restricted access describes a scope '
                                                                   'limitation, not grey box specifically'},
                                               'question': "What is 'grey box' penetration testing?",
                                               'wrong_explanations': {   'A': 'Lighting conditions are irrelevant to '
                                                                              'penetration testing.',
                                                                         'C': 'Combined automated/manual techniques '
                                                                              'describe a testing methodology, not '
                                                                              'grey box testing.',
                                                                         'D': 'Restricted access describes a scope '
                                                                              'limitation, not grey box '
                                                                              'specifically.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Scope defines exactly what is in-scope (can be tested) '
                                                              'and out-of-scope (must not be tested). Testing outside '
                                                              'scope is illegal — even if you have permission to test '
                                                              "one system, that doesn't authorise testing others.",
                                               'options': {   'A': 'The number of hours budgeted for the test — hours '
                                                                   'are part of engagement planning, not scope',
                                                              'B': 'The defined boundaries of the test — which '
                                                                   'systems, IP ranges, applications, and methods are '
                                                                   'authorised for testing',
                                                              'C': 'The severity of vulnerabilities to be tested — '
                                                                   'vulnerability severity is determined during '
                                                                   'testing — scope is decided upfront',
                                                              'D': 'The team size for the engagement — team size is a '
                                                                   'resource planning decision, not scope'},
                                               'question': "What is the 'scope' of a penetration test?",
                                               'wrong_explanations': {   'A': 'Hours are part of engagement planning, '
                                                                              'not scope.',
                                                                         'C': 'Vulnerability severity is determined '
                                                                              'during testing — scope is decided '
                                                                              'upfront.',
                                                                         'D': 'Team size is a resource planning '
                                                                              'decision, not scope.'}},
                                           {   'correct': 'B',
                                               'explanation': "Vulnerability management is not one-time — it's an "
                                                              'ongoing cycle: discover vulnerabilities, assess risk '
                                                              '(CVSS), prioritise by business impact, remediate, '
                                                              'verify fixes, and repeat. New vulnerabilities emerge '
                                                              'daily.',
                                               'options': {   'A': 'Managing the vulnerability scanner tool — managing '
                                                                   'the tool is tool administration — vulnerability '
                                                                   'management is the security process',
                                                              'B': 'A continuous cycle of identifying, classifying, '
                                                                   'prioritising, remediating, and verifying the '
                                                                   'remediation of vulnerabilities',
                                                              'C': 'Creating vulnerability reports for management — '
                                                                   'reporting is one step in the process — '
                                                                   'vulnerability management encompasses the full '
                                                                   'cycle',
                                                              'D': 'Managing the team responsible for vulnerability '
                                                                   'assessments — team management is an HR/management '
                                                                   'function — vulnerability management is the '
                                                                   'security process'},
                                               'question': "What is 'vulnerability management' as an ongoing process?",
                                               'wrong_explanations': {   'A': 'Managing the tool is tool '
                                                                              'administration — vulnerability '
                                                                              'management is the security process.',
                                                                         'C': 'Reporting is one step in the process — '
                                                                              'vulnerability management encompasses '
                                                                              'the full cycle.',
                                                                         'D': 'Team management is an HR/management '
                                                                              'function — vulnerability management is '
                                                                              'the security process.'}},
                                           {   'correct': 'B',
                                               'explanation': 'A good pentest report has two sections: (1) Executive '
                                                              'Summary (for management — business risk, key findings), '
                                                              '(2) Technical Details (for developers/engineers — exact '
                                                              'findings, exploitation steps, proof of concept, '
                                                              'remediation guidance).',
                                               'options': {   'A': 'To demonstrate that the organisation was tested — '
                                                                   'a report proving testing occurred is a compliance '
                                                                   'checklist — a proper report provides actionable '
                                                                   'findings',
                                                              'B': 'To document findings including exploited '
                                                                   'vulnerabilities, evidence, business impact, and '
                                                                   'prioritised remediation recommendations for both '
                                                                   'technical staff and management',
                                                              'C': 'A legal document indemnifying the testing company '
                                                                   '— liability is covered in the Rules of Engagement '
                                                                   '— not the report',
                                                              'D': 'A list of all tools used during the test — a tool '
                                                                   'list is a minor report appendix — the value is in '
                                                                   'findings and recommendations'},
                                               'question': "What is the purpose of a 'penetration test report'?",
                                               'wrong_explanations': {   'A': 'A report proving testing occurred is a '
                                                                              'compliance checklist — a proper report '
                                                                              'provides actionable findings.',
                                                                         'C': 'Liability is covered in the Rules of '
                                                                              'Engagement — not the report.',
                                                                         'D': 'A tool list is a minor report appendix '
                                                                              '— the value is in findings and '
                                                                              'recommendations.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Passive reconnaissance uses publicly available sources '
                                                              '— no direct interaction with target systems. The target '
                                                              'cannot detect it. Sources: Google, LinkedIn, Shodan, '
                                                              'WHOIS, DNS records, certificate transparency logs.',
                                               'options': {   'A': 'Reconnaissance that does not require a computer — '
                                                                   "computers are used — it's 'passive' because it "
                                                                   "doesn't touch target systems",
                                                              'B': 'Gathering information without directly interacting '
                                                                   'with the target — using OSINT, public DNS records, '
                                                                   'job listings, WHOIS',
                                                              'C': 'Reconnaissance that only uses passive network '
                                                                   'monitoring — passive network monitoring is a '
                                                                   'specific technique — passive reconnaissance is '
                                                                   'broader',
                                                              'D': "Reconnaissance conducted without the client's "
                                                                   'knowledge — authorisation level is defined by the '
                                                                   'engagement — not what makes reconnaissance '
                                                                   'passive'},
                                               'question': "What is 'passive reconnaissance' in penetration testing?",
                                               'wrong_explanations': {   'A': "Computers are used — it's 'passive' "
                                                                              "because it doesn't touch target "
                                                                              'systems.',
                                                                         'C': 'Passive network monitoring is a '
                                                                              'specific technique — passive '
                                                                              'reconnaissance is broader.',
                                                                         'D': 'Authorisation level is defined by the '
                                                                              'engagement — not what makes '
                                                                              'reconnaissance passive.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Active reconnaissance directly probes target systems — '
                                                              'Nmap port scans, banner grabbing, web crawling, DNS '
                                                              'zone transfers. Unlike passive recon, it generates '
                                                              'traffic that the target can detect and log.',
                                               'options': {   'A': 'Actively thinking about the target — active '
                                                                   'reconnaissance is technical probing — not just '
                                                                   'thinking about targets',
                                                              'B': 'Directly interacting with target systems to gather '
                                                                   'information — port scanning, service '
                                                                   'fingerprinting, web crawling — detectable by the '
                                                                   'target',
                                                              'C': 'Recruiting active informants about the target — '
                                                                   'recruiting informants is a human intelligence '
                                                                   '(HUMINT) technique — not technical active recon',
                                                              'D': 'Using automated scanners only (no manual '
                                                                   'techniques) — automation vs manual is not the '
                                                                   'distinction — direct interaction with target is'},
                                               'question': "What is 'active reconnaissance' in penetration testing?",
                                               'wrong_explanations': {   'A': 'Active reconnaissance is technical '
                                                                              'probing — not just thinking about '
                                                                              'targets.',
                                                                         'C': 'Recruiting informants is a human '
                                                                              'intelligence (HUMINT) technique — not '
                                                                              'technical active recon.',
                                                                         'D': 'Automation vs manual is not the '
                                                                              'distinction — direct interaction with '
                                                                              'target is.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Exploitation proves a vulnerability is real and shows '
                                                              'what an attacker could achieve — gaining a shell, '
                                                              'dumping credentials, escalating privileges. It provides '
                                                              'evidence for the report and demonstrates actual '
                                                              'business risk.',
                                               'options': {   'A': 'Writing an exploitation report for the client — '
                                                                   'report writing is post-exploitation documentation',
                                                              'B': 'Actively taking advantage of a vulnerability to '
                                                                   'gain unauthorised access or demonstrate the real '
                                                                   'impact of a security weakness',
                                                              'C': 'Identifying vulnerabilities using automated tools '
                                                                   '— identifying vulnerabilities is the '
                                                                   'scanning/assessment phase — exploitation is acting '
                                                                   'on findings',
                                                              'D': 'Extracting data from a database using SQL — sQL '
                                                                   'data extraction is one specific exploitation '
                                                                   'technique — exploitation is the broader phase'},
                                               'question': "What does 'exploitation' mean in penetration testing?",
                                               'wrong_explanations': {   'A': 'Report writing is post-exploitation '
                                                                              'documentation.',
                                                                         'C': 'Identifying vulnerabilities is the '
                                                                              'scanning/assessment phase — '
                                                                              'exploitation is acting on findings.',
                                                                         'D': 'SQL data extraction is one specific '
                                                                              'exploitation technique — exploitation '
                                                                              'is the broader phase.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Lateral movement: attackers use compromised systems as '
                                                              'stepping stones to reach other systems — using '
                                                              'pass-the-hash, stolen credentials, or exploiting trust '
                                                              'relationships between systems.',
                                               'options': {   'A': 'Moving a compromised laptop to a different '
                                                                   'location — physical relocation of devices is not '
                                                                   'lateral movement',
                                                              'B': 'After initial access, an attacker moves through '
                                                                   'the network — compromising additional systems to '
                                                                   'reach high-value targets',
                                                              'C': 'Changing the attack vector from web to network — '
                                                                   'changing attack vectors is attack pivoting — '
                                                                   'lateral movement specifically refers to network '
                                                                   'traversal',
                                                              'D': 'Spreading malware to multiple endpoints '
                                                                   'simultaneously — malware spreading is worm-like '
                                                                   'propagation — lateral movement is deliberate '
                                                                   'traversal toward objectives'},
                                               'question': "What is 'lateral movement' in the context of a cyber "
                                                           'attack?',
                                               'wrong_explanations': {   'A': 'Physical relocation of devices is not '
                                                                              'lateral movement.',
                                                                         'C': 'Changing attack vectors is attack '
                                                                              'pivoting — lateral movement '
                                                                              'specifically refers to network '
                                                                              'traversal.',
                                                                         'D': 'Malware spreading is worm-like '
                                                                              'propagation — lateral movement is '
                                                                              'deliberate traversal toward '
                                                                              'objectives.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Privilege escalation: vertical (user → admin) or '
                                                              'horizontal (user A → user B at same level). Attackers '
                                                              'escalate to gain more access — operating system '
                                                              'exploits, SUID binaries, token impersonation are common '
                                                              'techniques.',
                                               'options': {   'A': 'Increasing security team staff numbers — '
                                                                   'increasing staff is an HR function — privilege '
                                                                   'escalation is a technical attack phase',
                                                              'B': 'Gaining higher-level permissions than initially '
                                                                   'granted — e.g., from a standard user account to '
                                                                   'administrator/root',
                                                              'C': 'Escalating a security incident to senior '
                                                                   'management — escalating incidents is an incident '
                                                                   'response process — not privilege escalation',
                                                              'D': 'Upgrading to a more privileged security tool '
                                                                   'licence — software licensing is not privilege '
                                                                   'escalation'},
                                               'question': "What is 'privilege escalation'?",
                                               'wrong_explanations': {   'A': 'Increasing staff is an HR function — '
                                                                              'privilege escalation is a technical '
                                                                              'attack phase.',
                                                                         'C': 'Escalating incidents is an incident '
                                                                              'response process — not privilege '
                                                                              'escalation.',
                                                                         'D': 'Software licensing is not privilege '
                                                                              'escalation.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Post-exploitation shows what an attacker can do after '
                                                              'gaining a foothold: maintain persistence, move '
                                                              'laterally, dump credentials, exfiltrate data. This '
                                                              "demonstrates true business risk — not just 'I got in' "
                                                              "but 'here's what that means'.",
                                               'options': {   'A': 'Writing the final report after exploitation — '
                                                                   'report writing comes after the entire test — '
                                                                   'post-exploitation is still active testing',
                                                              'B': 'After gaining access, demonstrating impact — data '
                                                                   'exfiltration, persistence, lateral movement, '
                                                                   'showing what a real attacker would do with access',
                                                              'C': 'Patching vulnerabilities after they have been '
                                                                   'exploited — patching is remediation — the opposite '
                                                                   'of exploitation',
                                                              'D': 'Testing systems after they have been patched — '
                                                                   'testing after patching is remediation verification '
                                                                   '— not post-exploitation'},
                                               'question': "What is the purpose of 'post-exploitation' in penetration "
                                                           'testing?',
                                               'wrong_explanations': {   'A': 'Report writing comes after the entire '
                                                                              'test — post-exploitation is still '
                                                                              'active testing.',
                                                                         'C': 'Patching is remediation — the opposite '
                                                                              'of exploitation.',
                                                                         'D': 'Testing after patching is remediation '
                                                                              'verification — not post-exploitation.'}},
                                           {   'correct': 'B',
                                               'explanation': 'IDS monitors and alerts — it detects attacks '
                                                              '(signature-based or anomaly-based) and generates alerts '
                                                              'for investigation. It does NOT automatically block. An '
                                                              'IPS (Intrusion Prevention System) both detects and '
                                                              'blocks.',
                                               'options': {   'A': 'A system that blocks all suspicious traffic — '
                                                                   'automatically blocking is what an IPS does — IDS '
                                                                   'only detects and alerts',
                                                              'B': 'A system that monitors network/host activity for '
                                                                   'suspicious patterns and alerts administrators — '
                                                                   'detects attacks but does not automatically block '
                                                                   'them',
                                                              'C': 'A firewall with deep packet inspection — dPI '
                                                                   'firewalls are a type of firewall — IDS is a '
                                                                   'separate monitoring system',
                                                              'D': 'A system that prevents data exfiltration — data '
                                                                   'Loss Prevention (DLP) systems prevent exfiltration '
                                                                   '— different from IDS'},
                                               'question': "What is an 'IDS' (Intrusion Detection System)?",
                                               'wrong_explanations': {   'A': 'Automatically blocking is what an IPS '
                                                                              'does — IDS only detects and alerts.',
                                                                         'C': 'DPI firewalls are a type of firewall — '
                                                                              'IDS is a separate monitoring system.',
                                                                         'D': 'Data Loss Prevention (DLP) systems '
                                                                              'prevent exfiltration — different from '
                                                                              'IDS.'}},
                                           {   'correct': 'B',
                                               'explanation': 'SIEM (e.g., Splunk, IBM QRadar, Microsoft Sentinel) '
                                                              'collects logs from all sources (firewalls, servers, '
                                                              'endpoints, applications), correlates events to detect '
                                                              'threats, and provides alerting and forensic '
                                                              'investigation capabilities.',
                                               'options': {   'A': 'A physical security management system — physical '
                                                                   'security management uses different systems — SIEM '
                                                                   'is cybersecurity focused',
                                                              'B': 'A platform that aggregates, correlates, and '
                                                                   'analyses log/event data from across the '
                                                                   'organisation — enabling threat detection, '
                                                                   'investigation, and incident response',
                                                              'C': 'A tool specifically for vulnerability scanning — '
                                                                   'vulnerability scanners find weaknesses — SIEM '
                                                                   'monitors for active threats',
                                                              'D': 'A patch management system — patch management '
                                                                   'handles updates — SIEM handles security '
                                                                   'monitoring'},
                                               'question': 'What is SIEM (Security Information and Event Management)?',
                                               'wrong_explanations': {   'A': 'Physical security management uses '
                                                                              'different systems — SIEM is '
                                                                              'cybersecurity focused.',
                                                                         'C': 'Vulnerability scanners find weaknesses '
                                                                              '— SIEM monitors for active threats.',
                                                                         'D': 'Patch management handles updates — SIEM '
                                                                              'handles security monitoring.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Remediation verification closes the vulnerability '
                                                              'management loop — after patching, testers re-run the '
                                                              'specific test to confirm the fix works and that the '
                                                              "patch didn't introduce new issues.",
                                               'options': {   'A': 'Getting the vendor to verify their patch works — '
                                                                   'vendor verification is separate from your own '
                                                                   'testing — you must test your environment',
                                                              'B': 'Re-testing the previously vulnerable system to '
                                                                   'confirm the vulnerability has been successfully '
                                                                   'fixed and no new vulnerabilities were introduced',
                                                              'C': 'Documenting that remediation was completed — '
                                                                   'documentation records the action — re-testing '
                                                                   'confirms effectiveness',
                                                              'D': 'Notifying stakeholders that patching is complete — '
                                                                   'stakeholder notification is communication — '
                                                                   'verification is technical confirmation'},
                                               'question': "What is 'remediation verification' after a vulnerability "
                                                           'is patched?',
                                               'wrong_explanations': {   'A': 'Vendor verification is separate from '
                                                                              'your own testing — you must test your '
                                                                              'environment.',
                                                                         'C': 'Documentation records the action — '
                                                                              're-testing confirms effectiveness.',
                                                                         'D': 'Stakeholder notification is '
                                                                              'communication — verification is '
                                                                              'technical confirmation.'}},
                                           {   'correct': 'B',
                                               'explanation': 'Metasploit Framework provides: exploit modules, '
                                                              'payloads, auxiliary modules (scanning), and '
                                                              'post-exploitation tools. Used by pentesters to exploit '
                                                              'vulnerabilities and demonstrate impact in authorised '
                                                              'tests.',
                                               'options': {   'A': 'A vulnerability scanner that identifies weaknesses '
                                                                   'automatically — vulnerability scanners (Nessus, '
                                                                   'OpenVAS) identify weaknesses — Metasploit exploits '
                                                                   'them',
                                                              'B': 'An open-source exploitation framework providing '
                                                                   'tools to develop, test, and execute exploit code '
                                                                   'against target systems — used in penetration '
                                                                   'testing',
                                                              'C': 'A network packet analyser — packet analysis is '
                                                                   'done by Wireshark — Metasploit is for exploitation',
                                                              'D': 'A SIEM platform for security monitoring — sIEM '
                                                                   'platforms are monitoring tools — Metasploit is an '
                                                                   'exploitation framework'},
                                               'question': "What is 'Metasploit' and what is it used for?",
                                               'wrong_explanations': {   'A': 'Vulnerability scanners (Nessus, '
                                                                              'OpenVAS) identify weaknesses — '
                                                                              'Metasploit exploits them.',
                                                                         'C': 'Packet analysis is done by Wireshark — '
                                                                              'Metasploit is for exploitation.',
                                                                         'D': 'SIEM platforms are monitoring tools — '
                                                                              'Metasploit is an exploitation '
                                                                              'framework.'}}]}
def get_week_list():
    return [{"id": i, "name": name, "count": len(qs)} for i, (name, qs) in enumerate(QUESTIONS.items())]


@app.route("/")
def index():
    return render_template("index.html", weeks=get_week_list())


@app.route("/quiz/<week_param>")
def quiz(week_param):
    if week_param == "all":
        return render_template("quiz.html", week_name="All Weeks", week_id="all")
    try:
        week_id = int(week_param)
        weeks = list(QUESTIONS.keys())
        if week_id >= len(weeks):
            return "Not found", 404
        return render_template("quiz.html", week_name=weeks[week_id], week_id=week_id)
    except ValueError:
        return "Not found", 404


@app.route("/api/start/<week_param>")
def api_start(week_param):
    if week_param == "all":
        all_qs = []
        for qs in QUESTIONS.values():
            all_qs.extend(qs)
        random.shuffle(all_qs)
        qs_to_use = all_qs
        week_name = "All Weeks"
    else:
        weeks = list(QUESTIONS.keys())
        week_id = int(week_param)
        if week_id >= len(weeks):
            return jsonify({"error": "Not found"}), 404
        week_name = weeks[week_id]
        qs_to_use = list(QUESTIONS[week_name])
        random.shuffle(qs_to_use)

    # Shuffle the options within each question
    shuffled = []
    for q in qs_to_use:
        items = list(q["options"].items())
        random.shuffle(items)
        key_map = {}
        new_opts = {}
        for new_key, (old_key, val) in zip(["A","B","C","D"], items):
            new_opts[new_key] = val
            key_map[old_key] = new_key
        new_correct = key_map[q["correct"]]
        new_wrong = {key_map[k]: v for k, v in q.get("wrong_explanations", {}).items()}
        shuffled.append({
            "question": q["question"],
            "options": new_opts,
            "correct": new_correct,
            "explanation": q["explanation"],
            "wrong_explanations": new_wrong
        })

    qid = str(uuid.uuid4())
    session["qid"] = qid
    QUIZ_STORE[qid] = {"questions": shuffled, "index": 0, "score": 0, "answers": []}
    return jsonify({"total": len(shuffled), "week": week_name})


@app.route("/api/question")
def api_question():
    store = QUIZ_STORE.get(session.get("qid"), {})
    qs = store.get("questions", [])
    idx = store.get("index", 0)
    if idx >= len(qs):
        return jsonify({"done": True, "score": store.get("score", 0), "total": len(qs)})
    q = qs[idx]
    return jsonify({"number": idx + 1, "total": len(qs), "question": q["question"], "options": q["options"]})


@app.route("/api/answer", methods=["POST"])
def api_answer():
    data = request.json
    selected = data.get("answer")
    store = QUIZ_STORE.get(session.get("qid"), {})
    qs = store.get("questions", [])
    idx = store.get("index", 0)
    if idx >= len(qs):
        return jsonify({"error": "No question"}), 400
    q = qs[idx]
    correct = q["correct"]
    is_correct = selected == correct
    if is_correct:
        store["score"] = store.get("score", 0) + 1
    store["index"] = idx + 1
    answers = store.get("answers", [])
    answers.append({"question": q["question"], "selected": selected, "correct": correct, "is_correct": is_correct})
    store["answers"] = answers
    resp = {"correct": is_correct, "correct_answer": correct, "score": store["score"], "answered": idx + 1, "total": len(qs), "explanation": q["explanation"]}
    if not is_correct:
        resp["wrong_explanation"] = q.get("wrong_explanations", {}).get(selected, "")
    return jsonify(resp)


@app.route("/api/results")
def api_results():
    store = QUIZ_STORE.get(session.get("qid"), {})
    return jsonify({"score": store.get("score", 0), "total": len(store.get("questions", [])), "answers": store.get("answers", [])})


if __name__ == "__main__":
    total = sum(len(v) for v in QUESTIONS.values())
    print(f"\n  Cyber Security Quiz App — {total} questions across {len(QUESTIONS)} topics")
    print("  Open: http://localhost:5050\n")
    app.run(debug=False, port=5050, host="127.0.0.1")
