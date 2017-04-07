## Introduction to Security



## Security

Security as a field is huge.

* Cryptography (cryptology)
* Network security
* **Application security**
* Cybersecurity
* Lots of other interrelated categories


## So where do we start?

* Security concepts
* Mini case studies



## Zero-day

Unpatched vulnerability


## Threat model

* Commodity threat
* Advanced persistent threat

![security](https://imgs.xkcd.com/comics/security.png)


## Cryptographic primitives

* One-way hash functions
* Private key cryptography (symmetric cipher)
* Public key cryptography (asymmetric cipher)
* Signature


## Denial of service

Makes a service unresponsive



## Application security

### Input validation

Don't trust user input!

![bobby-tables](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)


### User input can be anything that comes from outside your application

* Cookies
* "Trusted" sources



## Case study: Insync web app

### Assets

* List of users
* Web app
* Desktop app
* Access tokens


### Attack vectors

* Web app itself
* Vulnerabilities on our servers (esp. zero-days)
* Vulnerabilities on Digital Ocean
* Us



## Case study: Insync licensing

### Assets

* Insync licenses


### Attack vectors

* Database modification
* Code modification
* Network filtering



## Cybersecurity tips

* 2FA
* Password manager
  - Avoid password reuse
  - Strong passwords
* Firewall
* Common sense ones
  - As developers, it's easier for us to spot threats
