
# game/indepth_displayables.rpy:15
translate japanese simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "Ren'PyにはDisplayableという概念があり、これは表示または非表示できる画像のようなものです。"

# game/indepth_displayables.rpy:22
translate japanese simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "imageステートメントによってDisplayableに画像名を与えられます。簡単な方法は単に画像ファイル名を指定することです。"

# game/indepth_displayables.rpy:29
translate japanese simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "しかしそれは画像が参照出来る唯一のものではありません。文字列にドットがなければ、Ren'Pyはそれを他の形式の画像として解釈します。"

# game/indepth_displayables.rpy:41
translate japanese simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "ブラウザーのcolorのように文字列に16進数の数値で構成されているカラーコードも含められます。"

# game/indepth_displayables.rpy:43
translate japanese simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "3または6桁の16進数は不透明で、赤、緑、青の値を含みます。4または8桁の16進数にはアルファが追加され、半透明にできます。"

# game/indepth_displayables.rpy:53
translate japanese simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "Transform DisplayableはDisplayableをとってそれに transform を適用します。"

# game/indepth_displayables.rpy:55
translate japanese simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "Displayableをとるということは、他の画像もとれるということです。実際ここで定義されたどのDisplayableもとれます。"

# game/indepth_displayables.rpy:63
translate japanese simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "カラーコードの文字列にはstyleプロパティーをとるより正式なSolid Displayableという書式があり、Solidのサイズを変更できます。通常画面を覆うのに使います。"

# game/indepth_displayables.rpy:72
translate japanese simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "テキストDisplayableはRen'Pyにテキストを画像であるかのように扱わせます。"

# game/indepth_displayables.rpy:80
translate japanese simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "つまり画像にするのと同様にTransformのような他のDisplayableをテキストに適用できます。"

# game/indepth_displayables.rpy:91
translate japanese simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "Composite Displayableは複数のDisplayableを下から上に重ねて1つにまとめます。"

# game/indepth_displayables.rpy:101
translate japanese simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "一部のDisplayableはRen'Pyのインターフェースをカスタマイズするのによく使われ、Frame Displayableはその1つです。Frame Displayableは他のDisplayableとその左、上、右、下の境界のサイズをとります。"

# game/indepth_displayables.rpy:111
translate japanese simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "Frame Displayableはそれが利用できる領域に合わせて拡大縮小します。これは四隅を同じサイズに保って中央を二次元、側面を一次元方向でスケーリングして行います。"

# game/indepth_displayables.rpy:118
translate japanese simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "Frameは設定されると、スケーリングせずに、Displayableの一部の敷き詰めもします。"

# game/indepth_displayables.rpy:126
translate japanese simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "Frameは概略では奇妙に見えるかもしれませんが、テクスチャーに使用すると、どうやって拡大縮小可能なインターフェースの要素を作っているか分かるでしょう。"

# game/indepth_displayables.rpy:132
translate japanese simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "これらは最も簡単なDisplayableですが、制作者が直接使用するほとんどとなります。"

# game/indepth_displayables.rpy:134
translate japanese simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "Pythonに詳しければ、ミニゲームのためにカスタムDisplayableの作成が出来ます。多くのビジュアルノベルではこれらで十分でしょうが。"

translate japanese strings:

    # game/indepth_displayables.rpy:67
    old "This is a text displayable."
    new "これはテキストDisplayableです。"
