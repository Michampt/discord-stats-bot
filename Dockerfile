FROM python
ADD bot.py /
ADD db /db
ADD cogs /cogs
ADD secrets.py /
ADD pypubg-fpp-mode /pypubg-fpp-mode
RUN cd /pypubg-fpp-mode && python setup.py build && python setup.py install
RUN pip install discord
CMD ["python", "bot.py"]
