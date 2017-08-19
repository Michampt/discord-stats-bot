FROM python
ADD bot.py /
ADD db /db
ADD cogs /cogs
ADD secrets.py /
RUN pip install discord pypubg
CMD ["python", "bot.py"]
