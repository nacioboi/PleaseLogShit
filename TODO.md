# How to go from here with `plsp`?

## TODO

### Top priority:

- [x] Write a few tests in some other projects to test its usability.
- [ ] Look at other more popular libs to see how ours stacks up and then add to this list accordingly.

  - I looked at the python built-in `logging` lib and it seems to be a good reference for how to structure the `plsp` lib.
  For example, they have it layed out with a `Logger` class that can contain:
    - A method of formatting the log messages.
    - A method of handling the log messages, i.e. where to send them.
    - A method of filtering the log messages, i.e. what to send.

Our `plsp` lib should have a similar structure.

### Once we're happy:

- [ ] Add a detailed documentation.
- [ ] Add a more generalized README.
- [ ] Add a `plsp` logo.
