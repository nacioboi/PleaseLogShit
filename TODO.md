# How to go from here with `plsp`?

## TODO

### Top priority:

- [ ] Write a few tests in some other projects to test its usability.
- [ ] Look at other more popular libs to see how ours stacks up and then add to this list accordingly.

## Compared against `loguru`:

- [ ] We need `loguru.logger.add` and `loguru.logger.remove` since its a great idea.
- [ ] Add a way to output encoded. This means each segment will be separated by some splitter. Then after, we can decode the
        raw and maybe, for e.g., sort by time, or sort by level, etc.
- [ ] Add a way to output structured data. I.e., `json` or `xml`.
- [ ] `loguru.logger.contextualize` is a good feature to add. It allows you to add context to the log messages. For example,
        If you have a multithreaded server, you can add the client id to the log messages.
- [ ] `loguru.logger.catch` is a good feature to add. It allows you to catch exceptions and log them.
- [ ] Incorporate cross-platform handlers like `LogtailHandler` and `LogzioHandler`.
- [ ] Add a way to capture the current state of variables via `pickle` and output them to a file. This will be useful for
        a scenario like, for e.g., a function that we cant attach to debugger and we struggling to get it to work,
        We can then output the state of the variables to a file and then see what's going on.

### Once we're happy:

- [ ] Add a detailed documentation.
- [ ] Add a more generalized README.
- [ ] Add a `plsp` logo.
