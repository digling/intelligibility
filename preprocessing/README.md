# Prepare Data for the Study

In order to test the code that we used for the final results, you do not need to run any of the code shown in this folder. But if you want to understand how we preprocessed the data, you should follow the instructions here.

We assume that you have access to a terminal and the regular tools installed there, including `curl`, `gunzip`, and `git`.

First, you can download the numberbatch vectors with the help of the Makefile we provide by typing:

```
make download-numberbatch
```

The basic data on German cognates can be downloaded with the following command:

```
make download-germancognates
```

To prepare trimmed versions of the cognates, first make sure to install all Python packages, by creating a new virtual environment and then typing:

```
make install-python
```

Then type:

```
make install-words
```

To prepare the final data: the vectors from numberbatch mapped on the data, type:

```
make prepare-vectors
```

