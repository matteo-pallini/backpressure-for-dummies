## Toy example of backpressure

This repo attempts to explain what backpressure is through a very simple example. I didn't find backpressure an obvious topic, and it took a while before (I think) it clicked for me. [This article](https://lucumr.pocoo.org/2020/1/1/async-pressure/) really helped to reach that point, and is also the main inspiration of this toy example.

This codebase contains a very simple service exposing 3 endpoints. Each one performs the same series of operations, but each implementation is slightly different:
1. `sync_endpoint` has the simplest possible implementation. A plain vanilla synchronous endpoint
2. `async_endpoint_without_backpressure` uses an asynchronous call with the IO bounded operation. This allows for other requests to be processed while pre-existing ones are blocked waiting for IO operations to be over. However, this endpoint has no mechanism to generate backpressure, so in real life once it receives too many requests it may just run out of memory or have requests waiting for a long time.
3. `async_endpoint_with_backpressure` uses an asynchronous call for the IO bounded operation, but also uses a semaphore to implement a mechanism to generate backpressure. If the service is already handling too many requests the semaphore will make it possible to send back straightaway a 429 and then let the client decide what to do.

The benefit of introducing aync calls to handle IO bounded operation should be obvious through the runtime of the blocking and async endpoints. However, backpressure is possibly harder to imagine, or at least it was for me. Here I tried to simulate backpressure by running the service in a docker container with a fairly low max memory available. So, given that each call requires an artificially large amount of memory, and requires a combination of CPU and IO bounded operations, once the service receives too many calls at the same time and has no backpressure mechanism the only thing it can do is collapse.

You can easily see that happening by running the service through the Dockerfile available
```bash
docker build . -t backpressure
docker run --rm -p 8080:80 --memory=200m backpressure
```

And then run in another tab a client call which will generate severall GET requests on the 3 endpoints described above.
```python
python -m backpressure_for_dummies.client
```
