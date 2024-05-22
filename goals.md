# Compared against `loguru`

## Power

The `loguru` package is known for being ready to use out of the box. It is really easy to use and somewhat powerful.

However, there is not as much customizability as I would like.

For example, `loguru` uses format strings, on the other hand, with our `plsp` package, we use an object oriented way of defining custom 'Logging Segment Generators'.

## Simplicity

Try to stay simple where possible.

This is because if its too hard to use or too complicated, the gains of power and customizability are outweighed by the complexity.

## Speed

We want to be able to use our library in production environments.

Because of this, we need to be taking advantage of the fastest possible methods of logging.

- `asyncio` for asynchronous logging,
- `numba` and `numpy` where possible for massive JIT speedups.
- `functools.cache` for caching expensive operations.
- And we shall top it all off with profiling our code and removing overhead.
  - Or, we could even try and combine operations into a single c function that we can call from python.

## Readability

Since this is not yet a popular library, we need to make sure that the code makes sense no matter who is reading it.

This will hopefully make it easier for people to contribute to the project.

For this we are going to use my `force_kwargs` package to make sure that keyword arguments are always passed in a consistent way.

> This may not be pythonistic, but it is a good way to ensure that the code is readable.
