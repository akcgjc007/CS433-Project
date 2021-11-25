titles = ["""Save plot to image file instead of displaying it using Matplotlib""",
          """What's the difference between a proxy server and a reverse proxy server?""",
          """Docker as a Proxy server for a web service""",
          """Storing C++ template function definitions in a .CPP file""",
          """What is the largest TCP/IP network port number allowable for IPv4?"""
          ]
descriptions = ["""I am writing a quick-and-dirty script to generate plots on the fly. I am using the code below (from Matplotlib documentation) as a starting point:

from pylab import figure, axes, pie, title, show

# Make a square figure and axes
figure(1, figsize=(6, 6))
ax = axes([0.1, 0.1, 0.8, 0.8])

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
fracs = [15, 30, 45, 10]

explode = (0, 0.05, 0, 0)
pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
title('Raining Hogs and Dogs', bbox={'facecolor': '0.8', 'pad': 5})

show()  # Actually, don't show, just save to foo.png
I don't want to display the plot on a GUI, instead, I want to save the plot to a file (say foo.png), so that, for example, it can be used in batch scripts. How do I do that?""", """What is the difference between a proxy server and a reverse proxy server?

""",
                """My app integrates with a web service that supports a proxy server. So I need to have integration tests that prove that works.

So I wanted to use Docker to create a local proxy server that I can run real integration tests to verify that my web service can be called through the proxy interface without errors.

So I tried https://github.com/jwilder/nginx-proxy

I started up the container with:

docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy
When I use it i get a 503 error 503 Service Temporarily Unavailable

Am I misunderstanding what this proxy does?
""", """I have some template code that I would prefer to have stored in a CPP file instead of inline in the header. I know this can be done as long as you know which template types will be used. For example:

.h file

class foo
{
public:
    template <typename T>
    void do(const T& t);
};
.cpp file

template <typename T>
void foo::do(const T& t)
{
    // Do something with t
}

template void foo::do<int>(const int&);
template void foo::do<std::string>(const std::string&);
Note the last two lines - the foo::do template function is only used with ints and std::strings, so those definitions mean the app will link.

My question is - is this a nasty hack or will this work with other compilers/linkers? I am only using this code with VS2008 at the moment but will be wanting to port to other environments.""", """What is the highest port number one can use?"""]
tags = [["python", "matplotlib", "plot"], [
    "proxy", "webserver", "terminology"], ["docker", "proxy"], ["c++", "templates"], ["tcp", "ipv4", "network-protocols"]]

answers = [["""While the question has been answered, I'd like to add some useful tips when using matplotlib.pyplot.savefig. The file format can be specified by the extension:

from matplotlib import pyplot as plt

plt.savefig('foo.png')
plt.savefig('foo.pdf')
Will give a rasterized or vectorized output respectively, both which could be useful. In addition, there's often an undesirable, whitespace around the image, which can be removed with:

plt.savefig('foo.png', bbox_inches='tight')
Note that if showing the plot, plt.show() should follow plt.savefig(), otherwise the file image will be blank.""", """As others have said, plt.savefig() or fig1.savefig() is indeed the way to save an image.

However I've found that in certain cases the figure is always shown. (eg. with Spyder having plt.ion(): interactive mode = On.) I work around this by forcing the closing of the figure window in my giant loop with plt.close(figure_object) (see documentation), so I don't have a million open figures during the loop:

import matplotlib.pyplot as plt
fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
ax.plot([0,1,2], [10,20,3])
fig.savefig('path/to/save/image/to.png')   # save the figure to file
plt.close(fig)    # close the figure window
You should be able to re-open the figure later if needed to with fig.show() (didn't test myself).""", """The solution is:

pylab.savefig('foo.png')""", """Just found this link on the MatPlotLib documentation addressing exactly this issue: http://matplotlib.org/faq/howto_faq.html#generate-images-without-having-a-window-appear

They say that the easiest way to prevent the figure from popping up is to use a non-interactive backend (eg. Agg), via matplotib.use(<backend>), eg:

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.plot([1,2,3])
plt.savefig('myfig')
I still personally prefer using plt.close( fig ), since then you have the option to hide certain figures (during a loop), but still display figures for post-loop data processing. It is probably slower than choosing a non-interactive backend though - would be interesting if someone tested that.

UPDATE: for Spyder, you usually can't set the backend in this way (Because Spyder usually loads matplotlib early, preventing you from using matplotlib.use()).

Instead, use plt.switch_backend('Agg'), or Turn off "enable support" in the Spyder prefs and run the matplotlib.use('Agg') command yourself."""], [
    """"The previous answers were accurate, but perhaps too terse. I will try to add some examples.

First of all, the word "proxy" describes someone or something acting on behalf of someone else.

In the computer realm, we are talking about one server acting on the behalf of another computer.

For the purposes of accessibility, I will limit my discussion to web proxies - however, the idea of a proxy is not limited to websites.

FORWARD proxy
Most discussion of web proxies refers to the type of proxy known as a "forward proxy."

The proxy event, in this case, is that the "forward proxy" retrieves data from another web site on behalf of the original requestee.

A tale of 3 computers (part I)
For an example, I will list three computers connected to the internet.

X = your computer, or "client" computer on the internet
Y = the proxy web site, proxy.example.org
Z = the web site you want to visit, www.example.net
Normally, one would connect directly from X --> Z.

However, in some scenarios, it is better for Y --> Z on behalf of X, which chains as follows: X --> Y --> Z.

Reasons why X would want to use a forward proxy server:
Here is a (very) partial list of uses of a forward proxy server:

1) X is unable to access Z directly because

a) Someone with administrative authority over X's internet connection has decided to block all access to site Z.

Examples:

The Storm Worm virus is spreading by tricking people into visiting familypostcards2008.com, so the system administrator has blocked access to the site to prevent users from inadvertently infecting themselves.

Employees at a large company have been wasting too much time on facebook.com, so management wants access blocked during business hours.

A local elementary school disallows internet access to the playboy.com website.

A government is unable to control the publishing of news, so it controls access to news instead, by blocking sites such as wikipedia.org. See TOR or FreeNet.

b) The administrator of Z has blocked X.

Examples:

The administrator of Z has noticed hacking attempts coming from X, so the administrator has decided to block X's IP address (and/or netrange).

Z is a forum website. X is spamming the forum. Z blocks X.

REVERSE proxy
A tale of 3 computers (part II)
For this example, I will list three computers connected to the internet.

X = your computer, or "client" computer on the internet
Y = the reverse proxy web site, proxy.example.com
Z = the web site you want to visit, www.example.net
Normally, one would connect directly from X --> Z.

However, in some scenarios, it is better for the administrator of Z to restrict or disallow direct access and force visitors to go through Y first. So, as before, we have data being retrieved by Y --> Z on behalf of X, which chains as follows: X --> Y --> Z.

What is different this time compared to a "forward proxy," is that this time the user X does not know he is accessing Z, because the user X only sees he is communicating with Y. The server Z is invisible to clients and only the reverse proxy Y is visible externally. A reverse proxy requires no (proxy) configuration on the client side.

The client X thinks he is only communicating with Y (X --> Y), but the reality is that Y forwarding all communication (X --> Y --> Z again).

Reasons why Z would want to set up a reverse proxy server:
1) Z wants to force all traffic to its web site to pass through Y first.
a) Z has a large web site that millions of people want to see, but a single web server cannot handle all the traffic. So Z sets up many servers and puts a reverse proxy on the internet that will send users to the server closest to them when they try to visit Z. This is part of how the Content Distribution Network (CDN) concept works.
Examples:
Apple Trailers uses Akamai
Jquery.com hosts its JavaScript files using CloudFront CDN (sample).
etc.
2) The administrator of Z is worried about retaliation for content hosted on the server and does not want to expose the main server directly to the public.
a) Owners of Spam brands such as "Canadian Pharmacy" appear to have thousands of servers, while in reality having most websites hosted on far fewer servers. Additionally, abuse complaints about the spam will only shut down the public servers, not the main server.
In the above scenarios, Z has the ability to choose Y.
""",
    """A pair of simple definitions would be:

Forward Proxy: Acting on behalf of a requestor (or service consumer)

Reverse Proxy: Acting on behalf of service/content producer.""",
    """I found the diagram below to be very helpful. It just shows the architecture of a forward vs. reverse proxy setup from client to server over the Internet. This image will help you to understand qyb2zm302's answer and other answers better.

Forward Proxy vs Reverse Proxy

You can also watch this video from F5's DevCentral by Peter Silva.

Picture Source: Quora. However, as per Martijn Pieters, this image could be from Pulse Secure Community or Julien Pauli's site (in French) at developpez.com.

It reminded me of the classic proverb:

A picture is worth 1000 words."""
], [
    """Although this has been resolved in the comments, I'll try to answer the following question:

Am I misunderstanding what this proxy does?

Yes. What your project requires, is the availability of a forward-proxy and what you are trying to use, is a reverse-proxy. This will become more clear once you go through the most top rated answers at Difference between proxy server and reverse proxy server

For a TL;DR moment:"""
], [
    """The problem you describe can be solved by defining the template in the header, or via the approach you describe above.

I recommend reading the following points from the C++ FAQ Lite:

Why can’t I separate the definition of my templates class from its declaration and put it inside a .cpp file?
How can I avoid linker errors with my template functions?
How does the C++ keyword export help with template linker errors?
They go into a lot of detail about these (and other) template issues.""",
    """For others on this page wondering what the correct syntax is (as did I) for explicit template specialisation (or at least in VS2008), its the following...

In your .h file...

template<typename T>
class foo
{
public:
    void bar(const T &t);
};
And in your .cpp file

template <class T>
void foo<T>::bar(const T &t)
{ }

// Explicit template instantiation
template class foo<int>;""",
    """This code is well-formed. You only have to pay attention that the definition of the template is visible at the point of instantiation. To quote the standard, § 14.7.2.4:

The definition of a non-exported function template, a non-exported member function template, or a non-exported member function or static data member of a class template shall be present in every translation unit in which it is explicitly instantiated.""",
    """Your example is correct but not very portable. There is also a slightly cleaner syntax that can be used (as pointed out by @namespace-sid, among others).

However, suppose the templated class is part of some library that is to be shared...

Should other versions of the templated class be compiled?

Is the library maintainer supposed to anticipate all possible templated uses of the class?

An Alternate Approach
Add a third file that is the template implementation/instantiation file in your sources.

lib/foo.hpp in/from library

#pragma once

template <typename T>
class foo
{
public:
    void bar(const T&);
};
lib/foo.cpp compiling this file directly just wastes compilation time

// Include guard here, just in case
#pragma once

#include "foo.hpp"

template <typename T>
void foo::bar(const T& arg)
{
    // Do something with `arg`
}
foo.MyType.cpp using the library, explicit template instantiation of foo<MyType>

// Consider adding "anti-guard" to make sure it's not included in other translation units
#if __INCLUDE_LEVEL__
  #error "Don't include this file"
#endif

// Yes, we include the .cpp file
#include <lib/foo.cpp>
#include "MyType.hpp"

template class foo<MyType>;
Of course, you can have multiple implementations in the third file. Or you might want multiple implementation files, one for each type (or set of types) you'd like to use, for instance.

This setup should reduce compile times, especially for heavily used complicated templated code, because you're not recompiling the same header file in each translation unit. It also enables better detection of which code needs to be recompiled, by compilers and build scripts, reducing incremental build burden.

Usage Examples
foo.MyType.hpp needs to know about foo<MyType>'s public interface but not .cpp sources

#pragma once

#include <lib/foo.hpp>
#include "MyType.hpp"

// Declare `temp`. Doesn't need to include `foo.cpp`
extern foo<MyType> temp;
examples.cpp can reference local declaration but also doesn't recompile foo<MyType>

#include "foo.MyType.hpp"

MyType instance;

// Define `temp`. Doesn't need to include `foo.cpp`
foo<MyType> temp;

void example_1() {
    // Use `temp`
    temp.bar(instance);
}

void example_2() {
    // Function local instance
    foo<MyType> temp2;

    // Use templated library function
    temp2.bar(instance);
}
error.cpp example that would work with pure header templates but doesn't here

#include <lib/foo.hpp>

// Causes compilation errors at link time since we never had the explicit instantiation:
// template class foo<int>;
// GCC linker gives an error: "undefined reference to `foo<int>::bar()'"
foo<int> nonExplicitlyInstantiatedTemplate;
void linkerError()
{
    nonExplicitlyInstantiatedTemplate.bar();
}
Note that most compilers/linters/code helpers won't detect this as an error, since there is no error according to C++ standard. But when you go to link this translation unit into a complete executable, the linker won't find a defined version of foo<int>.

If memory serves, I originally got the idea for this from SO. But when I wrote this answer, I could not for the life of me find that original SOA. Today, I think I found it: https://stackoverflow.com/a/495056/4612476

""",
    """This should work fine everywhere templates are supported. Explicit template instantiation is part of the C++ standard."""
], [
    """The port number is an unsigned 16-bit integer, so 65535.""",
    """The largest port number is an unsigned short 2^16-1: 65535

A registered port is one assigned by the Internet Corporation for Assigned Names and Numbers (ICANN) to a certain use. Each registered port is in the range 1024–49151.

Since 21 March 2001 the registry agency is ICANN; before that time it was IANA.

Ports with numbers lower than those of the registered ports are called well known ports; port with numbers greater than those of the registered ports are called dynamic and/or private ports.

Wikipedia : Registered Ports""",
    """As I understand it, you should only use up to 49151, as from 49152 up to 65535 are reserved for Ephemeral ports""",
]]
