label distribute:

    e "One thing Ren'Py makes easy is building distributions of your visual novel so you can give it to players."

    e "Before you build distributions, you should use the Lint command to check your game for problems."

    e "While not every potential problem lint reports is a real issue, they generally are, and you should try to understand what might be wrong."

    show launcher distribute at launcher_place
    with moveinleft

    e "After lint has finished, you can choose Build Distributions to build the Windows, Linux, and Mac distributions of your game."

    e "This can be as simple as clicking the Build button, when you're not on a Mac."

    e "If you are on a Macintosh, you can have Ren'Py sign the Mac application, which makes it easier for players to run. To enable this, you need to set build.mac_identity in options.rpy."

    hide launcher distribute
    with moveoutleft

    e "Ren'Py supports the mobile platforms, Android and iOS. We also support ChromeOS, through its ability to run Android apps."

    e "These mobile platforms can be a bit more complicated. While Android apps can be built everywhere, iOS requires a Mac."

    e "Mobile platforms might also require you to change your visual novel a little, due to the smaller limited devices. For example, buttons need to be made large enough for a person to touch."

    e "Rather than cover mobile here, I'll point you to the {a=https://www.renpy.org/doc/html/android.html}Android{/a} and {a=https://www.renpy.org/doc/html/ios.html}iOS{/a} documentation, where you can read more."

    e "Thanks to the distribution tools Ren'Py ships with, there are thousands of visual novels available."

    show eileen vhappy

    e "I hope that soon, yours will be one of them!"

    return
