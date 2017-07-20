
# ../tutorial_atl.rpyc:187
translate vietnamese tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "Trong hướng dẫn này, tôi sẽ chỉ bạn cách Ren'Py định vị sự vật trên màn hình như thế nào. Nhưng trước đó, chúng ta hãy cùng tìm hiểu một chút về cách Python xử lý các trị số."

# ../tutorial_atl.rpyc:189
translate vietnamese tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Có hai loại số chủ chốt trong Python: Số nguyên và số thực dấu phẩy động. Một số nguyên bao gồm toàn các chữ số, còn một số thực dấu phẩy động có một điểm thập phân."

# ../tutorial_atl.rpyc:191
translate vietnamese tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "Ví dụ, 100 là một số nguyên, thì 0.5 là một số thực dấu phẩy động, hoặc số động cho ngắn. Trong hệ thống này, có hai số 0: 0 là một số nguyên, và 0.0 là một số động"

# ../tutorial_atl.rpyc:193
translate vietnamese tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Py sử dụng số nguyên đại diện cho tọa độ tuyệt đối, và số động đại diện các phần phân đoạn của một khu vực có kích thước rõ ràng."

# ../tutorial_atl.rpyc:195
translate vietnamese tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "Khi chúng tôi đang định vị một cái gì đó, khu vực này thường là toàn bộ màn hình."

# ../tutorial_atl.rpyc:197
translate vietnamese tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "Tôi sẽ tránh ra một chút và cho bạn thấy một số vị trí đang có."

# ../tutorial_atl.rpyc:211
translate vietnamese tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "Vị trí gốc là góc trên bên trái của màn hình. Đó là nơi mà vị trí x (xpos) và vị trí y (ypos) đều là số không."

# ../tutorial_atl.rpyc:217
translate vietnamese tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "Khi chúng ta tăng xpos, chúng sẽ di chuyển về bên phải. Trị số hiện tại của xpos là .5, có nghĩa là một nửa chiều rộng trên màn hình."

# ../tutorial_atl.rpyc:222
translate vietnamese tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "Tăng xpos lên 1.0 sẽ di chuyển chúng đến góc bên phải của màn hình."

# ../tutorial_atl.rpyc:228
translate vietnamese tutorial_positions_80be064f:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 800 pixels across, using an xpos of 400 will return the target to the center of the top row."
    e "Chúng ta cũng có thể cho xpos một con số chính xác, bằng con số pixel được tính từ phía bên trái của màn hình. Ví dụ, nguyên cửa sổ này là 800 pixel, sử dụng một xpos 400 sẽ làm mục tiêu về điểm chính giữa phía trên. "

# ../tutorial_atl.rpyc:230
translate vietnamese tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "Các vị trí trục y-axis, hoặc ypos hoạt động theo cách tương tự. Ngay bây giờ, chúng tôi đang có trị số ypos 0.0."

# ../tutorial_atl.rpyc:236
translate vietnamese tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "Còn đây là vị trí ypos 0.5"

# ../tutorial_atl.rpyc:241
translate vietnamese tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "Một ypos 1.0 chỉ định một vị trí ở dưới cùng của màn hình. Nếu bạn nhìn kỹ, bạn có thể thấy vị trí điểm quay đang ở bên dưới cửa sổ văn bản."

# ../tutorial_atl.rpyc:243
translate vietnamese tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "Giống như xpos, ypos cũng có thể là một số nguyên. Trong trường hợp này, ypos sẽ cung cấp vị trí của tổng số pixel tính từ phía trên cùng của màn hình."

# ../tutorial_atl.rpyc:249
translate vietnamese tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "Bạn có thể đoán được vị trí này là ở đâu trên màn hình không?" nointeract

# ../tutorial_atl.rpyc:255
translate vietnamese tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Rất tiếc là sai rồi. xpos này là 0,75, và ypos là .25."

# ../tutorial_atl.rpyc:257
translate vietnamese tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "Nói cách khác, đó là 75 %% đường từ phía bên trái, và 25 %% đường từ đỉnh."

# ../tutorial_atl.rpyc:261
translate vietnamese tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "Tốt lắm! Bạn đã chọn đúng vị trí."

# ../tutorial_atl.rpyc:265
translate vietnamese tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Rất tiếc là sai rồi. Điểm xpos này là 0,75, và ypos là .25."

# ../tutorial_atl.rpyc:267
translate vietnamese tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "Nói cách khác, đó là 75 %% đường từ phía bên trái, và 25 %% đường từ đầu."

# ../tutorial_atl.rpyc:281
translate vietnamese tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "Vị trí thứ hai mà chúng ta cần quan tâm là anchor (điểm neo). Anchor là một điểm trên vật đang được định vị."

# ../tutorial_atl.rpyc:283
translate vietnamese tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "Ví dụ, ở đây chúng ta có một xanchor 0.0 và một yanchor 0.0. Đó là ở góc trên bên trái của hình ảnh logo."

# ../tutorial_atl.rpyc:288
translate vietnamese tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "Khi chúng ta tăng xanchor đến 1.0, điểm anchor sẽ di chuyển vào góc bên phải của hình ảnh."

# ../tutorial_atl.rpyc:293
translate vietnamese tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "Tương tự như vậy, khi cả hai xanchor và yanchor là 1.0, điểm anchor là góc dưới bên phải."

# ../tutorial_atl.rpyc:301
translate vietnamese tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "Để đặt một hình ảnh trên màn hình, chúng ta cần cả hai chỉ số vị trí và điểm anchor."

# ../tutorial_atl.rpyc:309
translate vietnamese tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "Sau đó chúng ta xếp chúng lên, do đó cả vị trí và anchor sẽ nằm trên cùng một điểm trên màn hình."

# ../tutorial_atl.rpyc:319
translate vietnamese tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "Khi chúng ta đặt cả hai ở góc trên bên trái, hình ảnh sẽ di chuyển đến góc trên bên trái của màn hình."

# ../tutorial_atl.rpyc:328
translate vietnamese tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "Với sự kết hợp của vị trí và anchor, bất cứ nơi nào trên màn hình cũng có thể được chỉ định, mà không cần quan tâm đến kích thước của hình ảnh."

# ../tutorial_atl.rpyc:340
translate vietnamese tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "Để cho tiện lợi xpos và xanchor thường được thiết lập để có cùng giá trị. Chúng tôi gọi đó là xalign, và nó mang lại một phân đoạn vị trí trên màn hình."

# ../tutorial_atl.rpyc:345
translate vietnamese tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "Ví dụ, khi chúng tôi đặt xalign 0.0, mọi thứ được sắp xếp ngay phía bên trái của màn hình."

# ../tutorial_atl.rpyc:350
translate vietnamese tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "Khi chúng ta đặt nó là 1.0, chúng được đưa ngay đến phía bên phải của màn hình."

# ../tutorial_atl.rpyc:355
translate vietnamese tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "Và khi chúng ta đặt nó là 0.5, chúng trở về trung tâm của màn hình."

# ../tutorial_atl.rpyc:357
translate vietnamese tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "yalign cũng tương tự, ngoại trừ dọc theo trục y-axis."

# ../tutorial_atl.rpyc:359
translate vietnamese tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "Nên nhớ xalign chỉ là thiết lập xpos và xanchor về cùng một giá trị, và yalign chỉ là thiết lập ypos và yanchor để về cùng một giá trị."

# ../tutorial_atl.rpyc:366
translate vietnamese tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "Một khi bạn hiểu được vị trí, bạn có thể sử dụng các lệnh chuyển động để di chuyển mọi thứ xung quanh màn hình Ren'Py."

# ../tutorial_atl.rpyc:373
translate vietnamese tutorial_atl_a1cc1bff:

    # e "While showing static images is often enough for most games, occasionally we'll want to change images, or move them around the screen."
    e "Thường thì hiển thị hình ảnh tĩnh là đủ cho hầu hết các trò chơi, nhưng thỉnh thoảng chúng ta muốn có một chút thay đổi hình ảnh, hoặc di chuyển chúng xung quanh màn hình."

# ../tutorial_atl.rpyc:375
translate vietnamese tutorial_atl_81dbb8f2:

    # e "We call this a Transform, and it's what ATL, Ren'Py's Animation and Transformation Language, is for."
    e "Chúng ta gọi điều này là Transform (chuyển động), và đó là những gì ATL có thể làm được, Ren'Py Animation and Transformation Language (ngôn ngữ chuyển động và hoạt ảnh Ren'Py)."

# ../tutorial_atl.rpyc:383
translate vietnamese tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "Nhưng trước tiên, chúng ta hãy hòa vào... buổi nhạc Rock Gratuitous !"

# ../tutorial_atl.rpyc:391
translate vietnamese tutorial_atl_3ccfe2ac:

    # e "That was a lot of work, and before you can do that, we'll need to start with the basics of using ATL."
    e  "Để làm được như vậy cần rất nhiều công sức, và trước khi bạn có thể làm được như thế, chúng ta sẽ đến với những điều cơ bản nhất của ATL."

# ../tutorial_atl.rpyc:393
translate vietnamese tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "Hiện tại có ba nơi mà ATL có thể được sử dụng trong Ren'Py."

# ../tutorial_atl.rpyc:397
translate vietnamese tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "Nơi ATL đầu tiên có thể được sử dụng là khi bạn gọi một hình ảnh. Thay vì cho việc hiển thị, một hình ảnh có thể được định nghĩa là một khối mã ATL."

# ../tutorial_atl.rpyc:399
translate vietnamese tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "Khi được sử dụng theo cách này, chúng ta phải chắc chắn rằng ATL bao gồm một hoặc nhiều ảnh hiển thị để thực hiện."

# ../tutorial_atl.rpyc:403
translate vietnamese tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "Cách thứ hai là thông qua việc sử dụng các lệnh transform. Lệnh này gán khối ATL cho một biến python, cho phép nó được sử dụng trong các đoạn mã và bên trong các hiệu ứng transform khác."

# ../tutorial_atl.rpyc:407
translate vietnamese tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "Cuối cùng, một khối ATL có thể được sử dụng như là một phần của lệnh show, thay vì lệnh at."

# ../tutorial_atl.rpyc:411
translate vietnamese tutorial_atl_c21bc1d1:

    # e "The key to ATL is what we call composeability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "Điểm chính của ATL là chúng ta có thể biên soạn được. ATL được tạo thành từ các lệnh tương đối đơn giản, có thể được kết hợp với nhau để tạo ra các hiệu ứng biến đổi phức tạp."

# ../tutorial_atl.rpyc:413
translate vietnamese tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "Trước khi tôi giải thích ATL làm việc như thế nào, hãy để tôi giải thích hình ảnh động và chuyển đổi transform."

# ../tutorial_atl.rpyc:418
translate vietnamese tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "Hoạt ảnh là khi biểu hiện cho thấy sự thay đổi. Ví dụ, ngay bây giờ tôi đang thay đổi biểu hiện của tôi."

# ../tutorial_atl.rpyc:445
translate vietnamese tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "Chuyển động liên quan đến việc di chuyển hoặc bóp méo hình ảnh. Điều này bao gồm việc đặt nó trên màn hình, phóng to phóng nhỏ, xoay nó, và thay đổi độ trong suốt của nó."

# ../tutorial_atl.rpyc:453
translate vietnamese tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "Đến với ATL, chúng ta hãy bắt đầu bằng cách nhìn vào một hình ảnh động đơn giản. Đây là một loại bao gồm năm dòng mã ATL, được chứa trong một hình ảnh."

# ../tutorial_atl.rpyc:455
translate vietnamese tutorial_atl_12c839ee:

    # e "In ATL, to change a displayable, simply mention it on a line of ATL code. Here, we're switching back and forth between two images."
    e "Trong ATL, để thay đổi một thể hiển thị, chỉ cần gọi nó trên một dòng mã ATL. Ở đây, chúng ta đang chuyển đổi qua lại giữa hai hình ảnh."

# ../tutorial_atl.rpyc:457
translate vietnamese tutorial_atl_c671ed7d:

    # e "Since we're defining an image, the first line of ATL has to name a displayable. Otherwise, there would be nothing to show."
    e "Vì chúng ta đang gọi lên một hình ảnh, dòng đầu tiên của ATL cần phải gọi tên của hình ảnh. Nếu không, sẽ không có gì để hiển thị."

# ../tutorial_atl.rpyc:459
translate vietnamese tutorial_atl_99386181:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half of a second each before continuing. That's how we give the delay between images."
    e "Dòng thứ hai và thứ tư là các câu lệnh tạm dừng, làm cho lệnh ATL tạm dừng một nửa giây trước khi tiếp tục. Đó là cách chúng tôi cho độ trễ giữa các hình ảnh."

# ../tutorial_atl.rpyc:461
translate vietnamese tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "Dòng cuối cùng là một lệnh lặp lại. Điều này làm cho khối hiện tại của ATL được khởi động lại. Bạn chỉ có thể có một câu lệnh lặp lại repeat cho mỗi khối."

# ../tutorial_atl.rpyc:466
translate vietnamese tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "Nếu chúng ta viết repeat 2 lần thì các hình ảnh động sẽ lặp hai lần, sau đó dừng lại."

# ../tutorial_atl.rpyc:471
translate vietnamese tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "Bỏ lệnh lặp lại có nghĩa là các hình ảnh động sẽ dừng lại một khi khối mã ATL đã chạy tới cuối đoạn code."

# ../tutorial_atl.rpyc:476
translate vietnamese tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "Theo mặc định, hình ảnh sẽ được thay thế ngay lập tức. Chúng ta cũng có thể sử dụng hiệu ứng chuyển đổi giữa các hình ảnh."

# ../tutorial_atl.rpyc:483
translate vietnamese tutorial_atl_a7f8ed01:

    # e "Now, let's move on to see how we can use ATL to transform an image. We'll start off by seeing what we can do to position images on the screen."
    e "Bây giờ, chúng ta hãy chuyển sang xem làm thế nào chúng ta có thể sử dụng ATL để di chuyển một hình ảnh. Chúng ta sẽ bắt đầu bằng cách xem những gì chúng ta có thể làm để định vị hình ảnh trên màn hình."

# ../tutorial_atl.rpyc:492
translate vietnamese tutorial_atl_24501213:

    # e "Perhaps the simplest thing we can do is to position the images on the screen. This can be done by simply giving the names of the transform properties, each followed by the value."
    e "Đơn giản nhất có lẽ là việc xác định vị trí hình ảnh. Điều này có thể được thực hiện bằng cách là gán tên của lệnh transform đã được xây dựng trước."

# ../tutorial_atl.rpyc:497
translate vietnamese tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "Thêm một vài lệnh, chúng ta có thể di chuyển chúng khắp màn hình."

# ../tutorial_atl.rpyc:499
translate vietnamese tutorial_atl_8b053b5a:

    # e "This code starts the image off at the top-right of the screen, and waits a second."
    e "Đoạn mã này bắt đầu bằng việc cho hình ảnh nằm ở phía trên bên phải màn hình và chờ đợi."

# ../tutorial_atl.rpyc:501
translate vietnamese tutorial_atl_d7fc5372:

    # e "It then moves it to the left side, waits another second, and repeats."
    e "Sau đó nó di chuyển xuống phía góc trái và đợi vài giây rồi lại tiếp tục như thế."

# ../tutorial_atl.rpyc:503
translate vietnamese tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "Các lệnh pause và repeat là những lệnh tương tự nhau mà chúng ta sử dụng trong hoạt cảnh này. Chúng chạy từ trên xuống trong đoạn code ATL."

# ../tutorial_atl.rpyc:508
translate vietnamese tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "Hình ảnh nhảy lung tung như thế không hoàn toàn có ích lợi cho lắm. Đó là lý do tại sao ATL có hàm nội suy (interpolation)."

# ../tutorial_atl.rpyc:510
translate vietnamese tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "Lệnh interpolation cho phép bạn dịch chuyển mượt mà hơn từ giá trị vị trí cũ đi đến vị trí mới."

# ../tutorial_atl.rpyc:512
translate vietnamese tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "Ở đây, chúng ta có một lệnh nội suy trên dòng ATL thứ hai. Bắt đầu với tên của một hàm thời gian, trong trường hợp này là một đường thẳng."

# ../tutorial_atl.rpyc:514
translate vietnamese tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "Sau một khoảng thời gian, trong trường hợp này là ba giây. Nó kết thúc bằng một danh sách các thuộc tính, ứng với các giá trị mới của nó."

# ../tutorial_atl.rpyc:516
translate vietnamese tutorial_atl_72d47fb6:

    # e "The old value is the value of the transform property at the start of the statement. By interpolating the property over time, we can change things on the screen."
    e "Các giá trị cũ là giá trị của chuyển động lúc bắt đầu. Bằng cách nội suy các thông số qua thời gian, chúng ta có thể thay đổi mọi thứ trên màn hình."

# ../tutorial_atl.rpyc:526
translate vietnamese tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL hỗ trợ các loại di chuyển phức tạp hơn, giống như vòng tròn và chuyển động cong. Nhưng tôi sẽ không hiển thị chúng ở đây."

# ../tutorial_atl.rpyc:528
translate vietnamese tutorial_atl_4a02c8d8:

    # e "Next, let's take a look at some of the transform properties that we can change using ATL."
    e "Tiếp theo, chúng ta hãy nhìn qua một số các chuyển động mà chúng ta có thể thay đổi bằng cách sử dụng ATL."

# ../tutorial_atl.rpyc:543
translate vietnamese tutorial_atl_821fcb91:

    # e "We've already seen the position properties. Along with xalign and yalign, we support the xpos, ypos, xanchor, and yanchor properties."
    e "Chúng ta đã nhìn thấy các thuộc tính vị trí. Cùng với xalign và yalign, chúng tôi hỗ trợ các thuộc tính xpos, ypos, xanchor, và yanchor."

# ../tutorial_atl.rpyc:558
translate vietnamese tutorial_atl_cca5082b:

    # e "We can perform a pan by using xpos and ypos to position images off of the screen."
    e "Chúng ta có sử dụng xpos và ypos để đưa hình ảnh ra khỏi cả màn hình."

# ../tutorial_atl.rpyc:560
translate vietnamese tutorial_atl_0394dd50:

    # e "This usually means giving them negative positions."
    e "Thường thì nó được xem đó là một định vị tệ khi không có mục đích rõ."

# ../tutorial_atl.rpyc:577
translate vietnamese tutorial_atl_2624662e:

    # e "The zoom property lets us scale the displayable by a factor, making it bigger and smaller. For best results, zoom should always be greater than 0.5."
    e "Lệnh zoom cho phép chúng ta điều chỉnh kích thước hình ảnh ở yếu tố lớn hơn và nhỏ hơn. Để có kết quả tốt nhất zoom nên lớn hơn 0.5"

# ../tutorial_atl.rpyc:591
translate vietnamese tutorial_atl_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoom và yzoom cho phép hình ảnh thay đổi kích thước tùy theo trục X hay trục Y."

# ../tutorial_atl.rpyc:602
translate vietnamese tutorial_atl_9fe238de:

    # e "The size property can be used to set a size, in pixels, that the displayable is scaled to."
    e "Thuộc tính size cho phép ta thiết đặt kích thước bằng pixel mà hình ảnh sẽ điều chỉnh ứng với nó."

# ../tutorial_atl.rpyc:617
translate vietnamese tutorial_atl_6b982a23:

    # e "The alpha property allows us to vary the opacity of a displayable. This can make it appear and disappear."
    e "Thuộc tính alpha cho phép chúng ta điều chỉnh độ trong suốt hình ảnh. Làm nó hiện lên và biến mất."

# ../tutorial_atl.rpyc:631
translate vietnamese tutorial_atl_60d6d9f3:

    # e "The rotate property lets us rotate a displayable."
    e "Thuộc tính rotate giúp chúng ta xoay hình ảnh."

# ../tutorial_atl.rpyc:633
translate vietnamese tutorial_atl_898a138a:

    # e "Since rotation can change the size, usually you'll want to set xanchor and yanchor to 0.5 when positioning a rotated displayable."
    e "Vì việc xoay như thế có thể làm thay đổi kích thước, thông thường bạn nên thiết đặt xanchor và yanchor 0.5 khi thực hiện xoay một hình ảnh."

# ../tutorial_atl.rpyc:644
translate vietnamese tutorial_atl_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "Thuộc tính crop cắt bỏ một khung hình ra khỏi hình ảnh và cho thấy một phần của ảnh gốc."

# ../tutorial_atl.rpyc:658
translate vietnamese tutorial_atl_ebb84988:

    # e "When used together, they can be used to focus in on specific parts of an image."
    e "Khi sử dụng chung với nhau, chúng có thể dùng để tập trung vào một phần của hình ảnh."

# ../tutorial_atl.rpyc:664
translate vietnamese tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "Ngoài các lệnh điều khiển hình ảnh, tạm dừng, nội suy và lặp lại có một vài lệnh chúng ta có thể dùng như một phần ATL."

# ../tutorial_atl.rpyc:678
translate vietnamese tutorial_atl_db6302bd:

    # e "When we create an ATL transform using the transform statement, we can use that transform as an ATL statement."
    e "Khi chúng ta tạo chuyển động ATL bằng lệnh transform, chúng ta có thể dùng transform đó như một lệnh ATL."

# ../tutorial_atl.rpyc:680
translate vietnamese tutorial_atl_785911cf:

    # e "Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "Vì vị trí mặc định cũng có thể coi là chuyển động, có nghĩa là các lệnh left, right và center cũng có thể sử dụng trong khối ATL."

# ../tutorial_atl.rpyc:698
translate vietnamese tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "Ở đây, chúng ta có hai dạng lệnh mới. Khối lệnh cho phép bạn bao gồm một khối mã ATL. Vì lệnh repeat cũng áp dụng đối với các khối, điều này cho phép bạn lặp lại chỉ một phần của chuyển động ATL."

# ../tutorial_atl.rpyc:700
translate vietnamese tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "Chúng tôi cũng có các lệnh thời gian (time), chạy sau khi số giây đã trôi qua từ khi bắt đầu của khối. Nó sẽ chạy ngay cả khi lệnh khác đang chạy, dừng các lệnh khác."

# ../tutorial_atl.rpyc:702
translate vietnamese tutorial_atl_30dc0008:

    # e "So this code will bounce the image back and forth for eleven and a half seconds, and then move back to the right side of the screen."
    e "Với đoạn mã này sẽ làm cho hình ảnh vào rồi ra trong mười một giây rưỡi, và sau đó di chuyển về phía bên phải của màn hình."

# ../tutorial_atl.rpyc:718
translate vietnamese tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "Lệnh parallel cho phép chúng ta chạy 2 khối mã ATL cùng một lúc."

# ../tutorial_atl.rpyc:720
translate vietnamese tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "Ở đây, khối mã trên làm cho hình ảnh di chuyển theo chiều ngang và khối mã dưới làm cho hình ảnh di chuyển theo chiều dọc. Vì chúng di chuyển với một tốc độ khác nhau, làm cho chúng cứ như đang nảy trên màn hình."

# ../tutorial_atl.rpyc:737
translate vietnamese tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "Cuối cùng, lệnh choice gọi Ren'Py chọn ra một khối mã ATL ngẫu nhiên. Điều này cho phép bạn thêm các lựa chọn mà Ren'Py có thể hiện lên."

# ../tutorial_atl.rpyc:743
translate vietnamese tutorial_atl_5fc8c0df:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out the ATL chapter in the reference manual."
    e "Hướng dẫn này chỉ mới là một phần nhỏ mà bạn có thể làm với ATL. Ví dụ như lệnh on và event chúng ta vẫn còn chưa nói tới. Để biết thêm chi tiết, bạn nên lên tìm đọc bộ hướng dẫn chương về ATL."

# ../tutorial_atl.rpyc:747
translate vietnamese tutorial_atl_1358c6b4:

    # e "But for now, just remember that when it comes to animating and transforming, ATL is the hot new thing."
    e "Nhưng hiện tại, chỉ cần nhớ là khi nói tới chuyển động và hoạt ảnh, phải nói tới ATL."

translate vietnamese strings:

    # game/tutorial_atl.rpy:249
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # game/tutorial_atl.rpy:249
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # game/tutorial_atl.rpy:249
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

