---
Title: "Orca Is the Free Cursor Killer Nobody's Talking About!"
Reference: "https://www.youtube.com/watch?v=-7V1NjDuoz4&t=124s"
Author: "Panda Making Money"
Created: "2026-07-11T12:54:46+09:00 2026-07-11T12:54:46+09:00"
Publisehd: "2026-07-03T12:47:55-07:00"
Tags:
  - "video"
  - "youtube"
ContentType: "Youtube"
Cover: "https://i.ytimg.com/vi/-7V1NjDuoz4/maxresdefault.jpg"
Keyword: "동영상, 공유, 카메라폰, 동영상폰, 무료, 올리기"
Processed: false
---
## 📝 자막 (Transcript)

![](https://www.youtube.com/watch?v=-7V1NjDuoz4)

This free tool runs 100 AI coding agents at once, on desktop and mobile. Meet Orca, the open source ADE developers are switching to.  
  
Orca is a free, open source agent development environment built by Stably, a Y Combinator backed team with engineering roots at Google Chrome and Uber. Instead of running one AI coding agent at a time inside a traditional editor, Orca lets you fan a single task across multiple agents like Claude Code, Codex, and Hermes Agent simultaneously, each working inside its own isolated git worktree, so you can compare results and merge the best one. This breakdown covers every major feature, including the mobile companion app for iOS and Android, Design Mode for pointing directly at UI elements instead of describing them, native GitHub and Linear integration, SSH worktrees for running agents on a remote server, and smart usage tracking across multiple agent accounts.  
  
If you're a developer looking for a genuine Claude Code alternative workflow or wondering whether an open source AI agent tool can actually replace Cursor, this video walks through the real strengths and the honest limitations, including current gaps in Linux packaging and cross agent pipelines. Whether you're managing one project or juggling several agents across a team, this is the clearest look yet at how parallel agent orchestration actually works in 2026.  
  
👉 Don't forget to like, subscribe, and hit the notification bell to stay updated with our latest videos!  
\=====================================================  
  
🔗 Try Orca (free & open source): https://onorca.dev/  
🔗 Orca on GitHub: https://github.com/stablyai/orca  
🖥️ Run agents remotely with Hostinger VPS: https://www.hostg.xyz/SHJEf  
  
\----------------------------------------------------------------------------------------------------------  
Timestamps:  
00:00:00 Introduction to Parallel AI Coding Agents  
00:02:04 What is Orca? An Agent Development Environment (ADE)  
00:03:02 Why the 'Orchestrating Agents' Concept Matters  
00:03:16 Open Source, Multi-Platform, and Rapid Growth  
00:04:05 Who Built Orca? The Stably Team Background  
00:05:52 Parallel Work Trees: The Core Feature  
00:07:51 Massive List of Supported Coding Agents  
00:09:12 Bring Your Own Subscription Model  
00:10:08 Mobile Companion App Features  
00:11:15 Understanding Mobile App Limitations  
00:12:03 Design Mode and Annotating Diffs  
00:14:03 GitHub and Linear Integration  
00:14:44 SSH Work Trees for Remote Machines  
00:16:13 Usage Tracking and Account Switching  
00:18:17 Comparison: Orca vs. Cursor vs. Ghosty  
00:20:14 Limitations and Room for Growth  
00:22:34 Final Summary and Verdict  
\----------------------------------------------------------------------------------------------------------  
  
🛠️ USEFUL TOOLS & SERVICES:  
  
📌 FREE 50 Pinterest Canva Templates - https://pandamakingmoney.systeme.io/freepinteresttemplates  
  
✅ PromoPDF AI - https://promopdfai.online/  
✅ Systeme.io - https://cutt.ly/fwC8IHCp  
✅ Shopify - https://shopify.pxf.io/DKgAgb  
\----------------------------------------------------------------------------------------------------------  
  
🎯 Follow us:  
Youtube - https://www.youtube.com/@PandaMakingMoney  
Pinterest - https://pinterest.com/lomashkumar111/  
Buy me a Coffee - https://www.buymeacoffee.com/PandaMakingMoney  
\=====================================================  
#aiagents #ai #tech  
\=====================================================  
  
Affiliate Disclosure:  
  
Please note that some of the links in this video description may be affiliate links. This means that if you click on one of these links and make a purchase, we may earn a commission at no additional cost to you.  
  
We only recommend products and services that we have personally used and believe will add value to our audience. Your support through these affiliate links helps us continue to provide valuable content on affiliate marketing and making money online.  
  
Thank you for your support! If you have any questions or concerns, feel free to reach out to us.

## Transcript

### Introduction to Parallel AI Coding Agents

**0:00** · Imagine opening one single app on your laptop and watching 10 different artificial intelligence agents write code for you at the exact same time.

**0:07** · Now, imagine checking on all of them from your phone while you were out getting coffee, getting a notification the moment one of them finishes a task, and then merging the best results straight into your project without ever touching a terminal window on your desk.

**0:20** · That is not a concept video or a future road map. That is a free and open-source tool called Orca, and it is already being used by developers who are tired of running one agent at a time and waiting around for it to finish. If you have spent any time working with tools like Claude Code, Codex, or any of the newer coding agents, you already know the biggest bottleneck is not the intelligence of the model anymore. It is the fact that you can usually only run one agent on one task at a time, sitting in one terminal window, while everything else waits in line. Orca throws that limitation out completely.

**0:50** · It lets you spin up a whole fleet of agents, each one working inside its own isolated workspace, all running in parallel, all inside a single clean interface built specifically for this exact workflow. In this video, we're going to break down everything Orca actually does. We will look at what makes it different from a normal code editor, who built it, and why their background actually matters here. And then we will go feature by feature through the tools that make this thing genuinely useful instead of just another flashy wrapper around a terminal.

**1:21** · That includes the parallel agent system, the mobile companion app that lets you control everything remotely, a surprisingly clever design tool, and the way it handles multiple agent accounts and usage limits automatically. We will also get into a full comparison against tools like Cursor, and by the end we'll talk honestly about where Orca still falls short, because no tool is perfect, and you deserve to know both sides before you install anything. Before we get into it, if you find this kind of breakdown useful, take a second to like this video and subscribe to the channel.

**1:50** · It genuinely helps this content reach more people who are trying to figure out which of these new artificial intelligence tools are actually worth their time. And sharing this with a friend or a co-worker who codes helps even more. All right, let's get into what Orca actually is and why so many developers have started talking about it. At its core, Orca describes itself as an agent development environment or an ADE. And that distinction actually matters more than it sounds.

### What is Orca? An Agent Development Environment (ADE)

**2:17** · A traditional code editor or integrated development environment was designed around one simple assumption. That a single human being is going to sit down, type code, and occasionally ask for help. Every part of that experience, from the file explorer to the terminal to the way tabs are organized, was built around one person doing one thing at a time. Orca flips that assumption on its head. Instead of being built for a human who occasionally uses an artificial intelligence assistant, it is built from the ground up for a human who is directing multiple artificial intelligence agents at once.

**2:48** · Almost like a manager overseeing a small team of developers rather than a single coder staring at a blinking cursor. The interface, the workflow, and every feature we are about to cover all stem from that one core idea. You're not writing code anymore. You are orchestrating agents that write code for you, reviewing their work, and deciding what gets merged. What makes this even more appealing is that Orca is completely free and fully open source, released under the MIT license, which is about as permissive as licensing gets.

### Why the 'Orchestrating Agents' Concept Matters

### Open Source, Multi-Platform, and Rapid Growth

**3:19** · You can look at every line of its code, modify it, or even build your own version if you wanted to. It runs on macOS, Windows, and Linux. So, unlike a lot of developer tools that quietly favor one operating system, Orca genuinely works across all three without forcing you into a specific ecosystem.

**3:37** · The project is also moving incredibly fast. As of recording this, Orca has crossed 11,100 stars on GitHub, and the team behind it is shipping new releases on a near daily basis. That kind of momentum is rare for a developer tool this early, and it usually signals one of two things, either a passing trend that fades in a few months or a genuine shift in how people are starting to work with these coding agents. Given everything we are about to show you, this looks a lot more like the second one.

**4:04** · Orca is built by a company called Stabley and knowing a little about the team behind it actually helps explain why the product feels as polished and fast-moving as it does. Stabley is backed by Y Combinator, which is one of the most well-known startup accelerators in the world and has helped launch companies that went on to become household names in the tech industry.

### Who Built Orca? The Stably Team Background

**4:25** · Getting into that program alone says something about how the broader startup world views what this team is building.

**4:31** · The people running the show are not newcomers to shipping software at scale, either. The chief executive built testing and release infrastructure that ships Google Chrome to billions of users around the world, which means she has direct experience with the kind of reliability and speed that a browser used by nearly everyone on the planet demands. The chief technology officer previously worked as one of the youngest technical leads at Uber, where he led large-scale machine learning projects on Uber's safety team. The kind of work where mistakes have real consequences and systems \[music\] need to actually hold up under pressure.

**5:02** · It is also worth knowing that Orca is not the only thing this team has built. They also run a separate product called Stabley, which is an artificial intelligence-powered testing platform that writes, runs, and maintains end-to-end tests inside continuous integration pipelines. That product exists specifically to help teams catch bugs and ship code with more confidence. And it shares a clear philosophy with Orca, using artificial intelligence not just to write code faster, but to make the entire development process more reliable at the same time.

**5:33** · So, when you put all of that together, what you're looking at is not a weekend side project or a random open-source repository that someone threw together over a few nights. Orca comes from a funded team with real engineering backgrounds at some of the biggest technology companies in the world. And that context is worth keeping in mind as we get into exactly what this tool can do. Now, let's get into the single feature that everything else in Orca is really built around, and that is parallel work trees. To understand why this matters, it helps to first understand what a work tree actually is in simple terms.

### Parallel Work Trees: The Core Feature

**6:06** · When you're working on a coding project, a work tree is basically a separate, isolated copy of your project's files and history that you can work in side without disturbing the main version of your code. Think of it like having several identical copies of the same house, where you can renovate one room in each copy completely independently, and none of the changes affect the others until you decide to bring one of them back into the original house. Orca takes this idea and builds an entire workflow around it.

**6:34** · Instead of giving one task to one agent and waiting for it to finish, you can take a single prompt, something like fix this bug or build this feature, and send it out to several different agents at the exact same time. With each agent working inside its own separate work tree. One agent might be running Claude code, another might be running Codex, and another might be running a completely different agent entirely, all tackling the same problem simultaneously, but in complete isolation from one another. Once all of the agents finish their work, you end up with several different solutions to compare side by side.

**7:04** · You can look at each approach, see which one actually solve the problem correctly, which one wrote cleaner code, and which one you trust the most, and then simply merge the version you like best directly into your project. The other attempts can be discarded without any cleanup headache, since they were never touching your main codebase to begin with. This is genuinely the feature that separates Orca from being just another wrapper around a terminal window. A lot of tools let you run one agent and watch it work.

**7:30** · Very few let you run several agents against the same problem at once, and treat the whole process almost like running a competition between them. If you have ever felt unsure whether an agent's first attempt at solving something was actually the best possible answer. This feature exists specifically to solve that uncertainty by letting you see multiple answers before committing to any of them. One of the things that makes Orca genuinely stand out is it just how many different coding agents it actually works with. And this is not a small curated list either.

### Massive List of Supported Coding Agents

**7:58** · Orca supports Claude Code, CodeX, Grok, Cursors command line agent, GitHub Copilot, Open Code, Amp, Open Claude, Anti-Gravity Pi, Hermes agent, Devin, Goose, Augie Charm Klein, Code Buff Continue, Droid, Kilo Code, Kimmy Kiro, Mistral Vibe, Quinn Code, Robo Dev, and honestly the list keeps going from there.

**8:18** · If you have been following this channel and watched our breakdowns on Hermes agent or Open Claude, both of those tools are fully supported inside Orca, which means everything we have already covered on this channel can slot directly into this parallel workflow. The real philosophy behind this massive list comes down to one simple rule. If an agent can run inside a terminal, Orca can run it.

**8:41** · Instead of building its own proprietary artificial intelligence model or locking you into one specific agent the way some competing tools do, Orca positions itself as a neutral environment that works with whatever you already use and whatever comes out next. When a new coding agent gets released next month, there's a very good chance it will work inside Orca on day one simply because of how the system is designed to plug into anything running in a terminal. This also ties directly into what might be the most practical part of the entire setup, the bring your own subscription model.

### Bring Your Own Subscription Model

**9:12** · Orca does not charge you extra to use these agents and does not act as a middleman reselling access to them. If you already pay for Claude Code or CodeX or any other agent, you simply connect your existing account inside Orca and start using it immediately. There's no second subscription stacked on top, no markup, and no new billing relationship to manage. You are paying the agent provider directly exactly the same as you already were. And Orca simply gives you a better environment to run everything inside of.

**9:41** · For anyone who has been experimenting with multiple agents already, maybe running Hermes agent for one project and Claude code for another, this solves a real annoyance. Instead of juggling separate terminal windows, separate setups, and separate mental contexts for each tool, everything lives inside one interface, with your existing subscriptions doing all the heavy lifting exactly like they were before.

**10:06** · Here is where Orca starts to feel like something genuinely different from a typical coding tool, because it comes with a fully functional mobile companion app available for both iPhone and Android. The idea behind it is simple.

### Mobile Companion App Features

**10:18** · Once you have several agents working away in the background on your desktop, you should not have to sit chained to your laptop just to keep an eye on them.

**10:25** · With the mobile app installed, you can check the live status of every agent that is currently running, see which ones have finished their tasks, and which ones might be stuck waiting on a decision from you. If an agent completes a task or runs into something it needs your input on, your phone gets a notification immediately, the same way you would get a message notification from any other app. That means you could be away from your desk entirely, grab a coffee, step out for lunch, and still know exactly what is happening with your agents in real time. The app also lets you send follow-up prompts directly from your phone.

**10:55** · So, if an agent finishes a task and you want to make an adjustment or move on to the next step, you do not need to run back to your desk to type it out. You can also switch between different connected accounts right from the mobile interface, which becomes especially useful if you're juggling multiple agent subscriptions across a team or multiple projects. Now, to be fully transparent here, there's an important detail worth understanding before you get too excited about this.

### Understanding Mobile App Limitations

**11:21** · The mobile app is a companion to the desktop app, not a fully stand-alone experience. That means your desktop needs to actually be running and connected for the mobile app to work, either over your local network or through a relay connection provided by Stabley. So, if you close your laptop completely, your phone will not be able to see or control anything since there is no active desktop session for it to connect to. It is less like having agents living entirely in the cloud and more like having a remote control for a session that is still running back on your machine.

**11:49** · Once you understand that limitation, though, it is still an incredibly convenient way to stay connected to your agents without being physically tied to your desk all day.

**11:59** · Two of the smaller, but genuinely clever features inside Orca are design mode and the ability to annotate diffs directly.

### Design Mode and Annotating Diffs

**12:06** · And both of them solve problems that anyone who has worked closely with a coding agent will immediately recognize.

**12:12** · Let's start with design mode. Normally, if you want an agent to fix something about how your website or application looks, you end up describing it in words, something like make the button in the top-right corner a little bigger and change its color to blue. The problem is that translating a visual detail into a text description is clumsy and agents often misunderstand exactly which element you're talking about, especially on a page with a lot of similar-looking components. Design mode solves this by letting you literally click on the element inside a live browser preview running right inside Orca.

**12:41** · The moment you click it, Orca automatically grabs that element's actual code, its styling information, and a cropped screenshot showing exactly what you clicked and sends all of that straight into the agent's prompt. Instead of describing what you want changed, you're pointing directly at it, and the agent receives technical details it needs without any guesswork involved.

**13:02** · The second feature works alongside your normal review process, and it lets you annotate an agent's code changes directly on individual lines, almost the same way you would leave a comment on a pull request inside GitHub. If an agent makes a change and you notice a line that needs adjusting, you could drop a comment right on that specific line explaining what needs to happen, and that comment gets sent straight back to the agent so it can revise its own work.

**13:27** · This entire back and forth happens without ever needing to leave Orca or open a separate browser tab to manage the review process somewhere else.

**13:36** · Together, these two features change how review actually feels day-to-day.

**13:40** · \[music\] Instead of scrolling through a wall of code trying to explain problems in vague sentences, you are pointing at exact visual elements and leaving precise comments on exact lines of code. And the agent understands both with a level of accuracy that plain text instructions usually cannot match. It's a small shift in how you communicate with these agents, but it removes a surprising amount of friction from the review process. Orca also builds in native integration with two tools that most development teams already rely on heavily, GitHub and Linear.

### GitHub and Linear Integration

**14:08** · Instead of switching over to a browser tab every time you need to check a pull request or look at what tasks are assigned to you.

**14:17** · Orca lets you browse issues, pull requests, and project boards directly inside the app itself. You can open a task from Linear, spin up a work tree for it immediately, and have an agent start working on it without ever leaving the environment you're already in. For teams that live inside these two tools daily, this removes one of the more annoying context switches in the entire development workflow, jumping back and forth between your code editor and your browser just to check what you were supposed to be working on next. The other major feature here is SSH work trees, and this one is aimed at a slightly more advanced use case.

### SSH Work Trees for Remote Machines

**14:51** · Normally, if you wanted to run your coding agents on a more powerful remote server instead of your local laptop, you would usually end up living inside a browser-based development environment to do it. Something like CodeSpaces or Gitpod. Orca offers an alternative to that by letting you connect to a remote machine over SSH while still keeping the full desktop experience. Meaning you get the polish and responsiveness of a native app, but the actual heavy lifting of running your agent happens on a beefier remote box instead of your local machine.

**15:18** · This is particularly useful if you want to run several resource-hungry agents at once without draining your laptop's battery or maxing out its memory. Or if you simply want your agent workflow to keep running on a server even when your laptop is closed. It is worth mentioning here that if you're looking for an affordable remote server to run something like this on, Hostinger's virtual private servers are solid option worth checking out. And we will drop a link in the description if you want to explore that. Now, one honest detail worth understanding about SSH Worktrees before you try to set this up on any random remote machine.

**15:49** · This is not compatible with just any SSH server you happen to have access to. Orca actually needs to install a small piece of its own software on that remote box first in order for the connection to work properly. It is a straightforward one-command setup and it is documented clearly, but it's still worth knowing up front, especially if you're trying to connect to a lockdown corporate server where installing anything additional might not be allowed.

### Usage Tracking and Account Switching

**16:13** · This next feature might not sound as exciting as some of the others at first, but if you have been using coding agents seriously over the past couple of months, you have probably already run into the exact problem it solves. Both Anthropic and OpenAI tightened their rate limits and usage tiers recently. And that means hitting a wall in the middle of the task has become a much more common and much more frustrating experience for a lot of developers. Orca deals with this by building account switching and live usage tracking directly into the interface.

**16:42** · If you have multiple accounts connected, whether that is separate Claude accounts or separate Codex accounts, you can hot swap between them instantly without having to log out and log back in every single time. On top of that, Orca shows you your actual usage numbers and exactly when your rate limits are going to reset right there in the interface, so you're never caught off guard by suddenly losing access in the middle of task. This becomes especially important once you start actually using the parallel Worktree feature we talked about earlier.

**17:11** · Remember, if you fan a single prompt out across three different agents running at the same time, you're not using one unit of your usage allowance, you're using three. Since each agent is consuming its own separate share of your quota simultaneously. A lot of new users get genuinely surprised by this the first time it happens, expecting the usage to last just as long as it normally would with a single agent, only to find their limit hit far sooner than expected simply because they had multiple agents running in parallel. Having clear visibility into this changes how you actually plan your work.

**17:42** · Instead of running agents blindly and hoping you do not hit a wall halfway through an important task, you can glance at your usage numbers, see how much room you actually have left, and decide whether now is the right moment to fan a task out across several agents, or whether it makes more sense to stick with just one until your limits reset. It is a small feature on the surface, but once you have felt the frustration of an agent stopping mid-task because you ran out of usage, you understand exactly why the team decided to build this in from the start.

**18:12** · At this point, you might be wondering how Orca actually stacks up against tools you have probably already heard of, specifically Cursor and Ghosty, since those are the two comparisons that come up most often when people talk about this space. Let's start with Cursor. Cursor is a tightly integrated coding editor that comes with its own built-in artificial intelligence baked directly into the product. It is polished, it is popular, and for a lot of developers who just want one really good agent working inside a familiar editor, it does the job extremely well.

### Comparison: Orca vs. Cursor vs. Ghosty

**18:41** · The trade-off is that Cursor is built around the idea of one agent at a time working inside its own ecosystem. It is not really designed around the idea of running several different agents from several different providers all at once, and is not built with parallel workflows or a mobile companion in mind the way Orca is. Ghosty, on the other hand, is a fast and modern terminal application, and it comes up in this comparison because a lot of developers who run coding agents from the command line rely heavily on a good terminal experience to do it.

**19:10** · Ghosty is genuinely excellent at what it does, but it is fundamentally still just a terminal. It gives you fast, responsive split panes and a clean interface for running commands, but it does not manage work trees for you. It does not give you a mobile app, and it does not know anything about tracking usage across multiple agent accounts.

**19:28** · It's a piece of the puzzle, not the whole environment. This is really where Orca's entire pitch comes together. If what you want is one deeply integrated agent inside a familiar coding editor, Cursor is still going to be a fantastic choice, and there's nothing wrong with sticking with it. But, the moment you want to run more than one agent at a time, the moment you want to compare different agents against the same problem, or the moment you want to check on your agents from your phone instead of being stuck at your desk, that is exactly the situation Orca was built for. It does not try to replace your terminal or compete with Cursor's built-in intelligence.

**19:59** · It sits one level above both of them, acting as the environment that manages and orchestrates everything else, whether that is Cursor's own command-line agent, Quad Code, or any other tool you already use. Now, as much as we have talked about what makes Orca genuinely impressive, it would not be a fair breakdown if we did not spend a few minutes on where it actually falls short, because there are some real limitations worth knowing about before you build your entire workflow around it.

### Limitations and Room for Growth

**20:25** · The first thing worth mentioning is that Orca is built as an Electron-based application rather than something lighter like Tauri. In practical terms, that means the app itself carries a bit more weight than some of its competitors, with a noticeably larger install size and higher idle memory usage once you have a few agents running at the same time. For most modern laptops, this is not going to be a deal breaker, but if you're working on an older machine or one with limited memory to begin with, it's something you will likely notice. Second, if you're running Linux, support right now comes only in the form of an AppImage.

**20:57** · There is no .deb package, no .rpm package, and no Snap or Flatpak version available yet.

**21:05** · The AppImage format does work across most Linux distributions without much trouble, but it does not integrate quite as smoothly into your system as a proper native package would. So, Linux users should go in expecting a slightly rougher edge compared to the Mac OS and Windows experience. Third, and this is probably the most requested feature that simply is not here yet. There is no true cross agent pipeline system built in.

**21:29** · What that means is you cannot currently set up a chain where, for example, one agent plans out a feature, a second agent writes the test for it, and a third agent implements the actual code, all automatically handing off to each other in sequence. Right now, the parallel work tree system lets you run multiple agents on the same task at once, but true multi-step pipelines where different agents each handle a different part of the process are still on the road map, rather than something you can use today. Lastly, if you're on Android, know that support tends to lag slightly behind iOS.

**21:59** · With new mobile features typically showing up on the iPhone app first before making their way over to Android in a following release.

**22:07** · None of these downsides are deal breakers on their own, and honestly most of them are the kind of thing you would expect from a tool that is still moving this fast and shipping new releases nearly every single day. But going in with realistic expectations rather than assuming it is a flawless piece of software will save you some frustration, especially if you were hoping for full Linux packaging or automated multi-agent pipelines right out of the box.

**22:28** · So, that is the full breakdown of Orca, a free and open-source agent development environment that genuinely rethinks what it means to work with coding agents instead of just wrapping a nicer interface around a single terminal window. We covered what makes it fundamentally different from a normal code editor, the team behind it, and why their background actually matters. The parallel work tree system that lets you run multiple agents against the same problem at once. The massive list of agents it supports, including tools we have already covered on this channel like Hermes agent.

### Final Summary and Verdict

**22:59** · The mobile companion app that lets you stay connected from anywhere. Design mode and diff annotations that make reviewing agent work faster and more precise. Native GitHub and linear integration. SSH work trees for running things on a remote machine. Smart account switching and usage tracking. And finally, an honest look at where it still has room to grow.

**23:19** · If you do decide to try running your agents on a remote server, especially if you're experimenting with those SSH work trees we talked about earlier, hosting is virtual private servers are genuinely solid and affordable option. Spin one up quickly and you'll find that link down in the description below if you want to check it out. At the end of the day, whether Orca is the right fit for you really comes down to how you already work. If you're a perfectly happy running one agent at a time inside a tool like Cursor, there's nothing wrong with sticking exactly where you are.

**23:45** · But if you have ever wished you could compare a few different approaches to the same problem side-by-side, or want to check on your agents without being chained to your desk all day, this is genuinely worth downloading and trying for yourself, especially considering not cost you anything to do it. If this video helped you understand what Orca actually does, do me a favor and drop a like on it. And subscribe if you have not already, since we cover tools exactly like this one on a regular basis.

**24:11** · Let me know down in the comments which agent you would run first inside Orca, and whether you're team Claude code, team Codex, or something else entirely. Thanks for watching and I will see you in the next one.