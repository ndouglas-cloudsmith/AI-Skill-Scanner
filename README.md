# AI-Skill-Scanner
Simple tool for scanning Indicators of Compromise (IoCs) in publicly-source AI Skills in Github repositories


## Using Skill Scanner

Searching the ```openclaw``` skills repository for cryptominers - ie: ```xmrig```
```
python3 skillscanner.py --source openclaw/skills --search xmrig
```

Searching the ```alirezarezvani/claude-skills``` repo for skills that could be exploiting known vulnerabilities - ie: ```CVE-```
```
python3 skillscanner.py --source alirezarezvani/claude-skills --search cve-
```
