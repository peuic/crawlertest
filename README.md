# Projudi Crawler

Crawler created to gather data from lawsuits hosted on the Projudi-Ba platform.

Code Files:
- Chalkboard.py

Used for testes and implementations of new features on the crawler/parser.

- Pjrequest.py

Used to search the Projudi for the lawsuits IDs that'll be used to request the data and then parser it with Ditto.

- Ditto.py

Uses the list generated on Pjrequest.py to search for the ids, gather the lawsuits data and parser them to store the info.
