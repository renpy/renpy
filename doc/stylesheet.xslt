<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
  <!-- First, copy the element. -->
  <xsl:template match="*" priority="-1">
    <xsl:copy>
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>
  
  <!-- Now, handle some elements specially. -->
  
  <xsl:template match="doc">
    <html>
      <head>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title><xsl:value-of select="title" /></title>
      </head>
      <body>
        <xsl:apply-templates />
      </body>
    </html>
  </xsl:template>

  <xsl:template match="toc">
    <ol>
      <xsl:for-each select="../h3">
        <li>
          <a>
            <xsl:attribute name="href">#<xsl:value-of select="." /></xsl:attribute>
            <xsl:value-of select="."/>
          </a>
        </li>
      </xsl:for-each>
    </ol>
  </xsl:template>

  <xsl:template match="funcindex">
    <ul>
      <xsl:for-each select="//function">
        <xsl:sort select="@name" />
        <li>
          <a>
            <xsl:attribute name="href">#<xsl:value-of select="@name" /></xsl:attribute>
            <xsl:value-of select="@name"/>
          </a>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="varindex">
    <ul>
      <xsl:for-each select="//var">
        <xsl:sort select="@name" />
        <li>
          <a>
            <xsl:attribute name="href">#<xsl:value-of select="@name" /></xsl:attribute>
            <xsl:value-of select="@name"/>
          </a>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="styleindex">
    <ul>
      <xsl:for-each select="//renpy_style">
        <xsl:sort select="@name" />
        <li>
          <a>
            <xsl:attribute name="href">#<xsl:value-of select="@name" /></xsl:attribute>
            <xsl:value-of select="@name"/>
          </a>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="propindex">
    <ul>
      <xsl:for-each select="//prop">
        <xsl:sort select="@name" />
        <li>
          <a>
            <xsl:attribute name="href">#<xsl:value-of select="@name" /></xsl:attribute>
            <xsl:value-of select="@name"/>
          </a>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template match="h3">
    <a>
      <xsl:attribute name="name"><xsl:value-of select="." /></xsl:attribute>
      <h3><xsl:apply-templates /></h3>
    </a>
  </xsl:template>

  <xsl:template match="title">
    <h1><xsl:apply-templates /></h1>
  </xsl:template>

  <xsl:template match="subtitle">
    <h2><xsl:apply-templates /></h2>
  </xsl:template>

  <xsl:template match="def">
    <b><i><xsl:apply-templates /></i></b>
  </xsl:template>

  <xsl:template match="example">
    <pre class="example"><xsl:apply-templates /></pre>
  </xsl:template>

  <xsl:template match="rule">
    <div class="rule"><xsl:apply-templates /></div>
  </xsl:template>

  <xsl:template match="function">
    <a><xsl:attribute name="name"><xsl:value-of select="@name" /></xsl:attribute></a>
    <table>
      <tr>
        <td valign="top" class="funcname"><xsl:value-of select="@name" /></td>
        <td class="funcsig"><xsl:value-of select="@sig" />:</td>
      </tr>
    </table>
    <div class="funcbody">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="param">
    <span class="param"><xsl:apply-templates /></span>
  </xsl:template>

  <xsl:template match="prop">
    <a><xsl:attribute name="name"><xsl:value-of select="@name" /></xsl:attribute></a>
    <p class="prop">
      <span class="propname"><xsl:value-of select="@name" /></span>
      --- <xsl:apply-templates />
    </p>
  </xsl:template>

  <xsl:template match="renpy_style">
    <a><xsl:attribute name="name"><xsl:value-of select="@name" /></xsl:attribute></a>
    <dt><b><xsl:value-of select="@name" /></b>:</dt>
    <dd><xsl:apply-templates /></dd>
  </xsl:template>

  <xsl:template match="renpy_style_inherits">
    (inherits from <b><xsl:apply-templates /></b>) <br />
  </xsl:template>

  <xsl:template match="var">
    <a><xsl:attribute name="name"><xsl:value-of select="@name" /></xsl:attribute></a>
    <dt class="var"><b><xsl:value-of select="@name" /></b> = <xsl:value-of select="@value" /></dt>
    <dd>
      <xsl:apply-templates />
    </dd>
  </xsl:template>
    
</xsl:stylesheet>