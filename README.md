### Python raytracer
Firstly, I must credit the [Raytracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html) Series for it's great help with the math to make this possible.
Without the series there's no way I would have been able to figure this all out on my own, so thank you to Peter Shirley, Trevor David Black, Steve Hollasch for writing that and making it available for free online.

### Performance disclaimer
There's just no way to make a python raytracer more performant than one written in a compiled language like C++, but I've done my best to at least make it manageable with techniques like multithreading. Disabling the GIL should be okay for this project and it will help a lot.
Make sure to allocate as many cores as possible, but to be honest the bottleneck is not the CPU, it's just retrieving all the type data and variables from memory. I believe the thread count only helps because it makes it so that multiple memory transfers can run at once so they can be run in parallel and not sequentially, so it may be beneficial to even put more threads than you have cpu cores but I haven't tested this too extensively.

Good luck!

## Possible future additions
Mixture densities and light scattering from the book
Some sort of JSON or other way to enter the scene rather than just the CLI.
