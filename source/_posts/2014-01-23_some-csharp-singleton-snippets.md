date: 2014-01-23 18:31
title: 几个C#单例模式的Snippet
permalink: some-csharp-singleton-snippets
tags: [csharp,dev]
---

其实本来不大想做这几个Snippet，但是看了一下ReSharper里面的Template Explorer实在是用起来怪怪的，官方文档又说得不清不楚的。只好先从VS里面自带的模板弄出几个Snippet，模仿着写了四个Singleton，下面贴一下吧。

1. 静态初始化单例

        <?xml version="1.0" encoding="utf-8" ?>
        <CodeSnippets  xmlns="http://schemas.microsoft.com/VisualStudio/2005/CodeSnippet">
            <CodeSnippet Format="1.0.0">
                <Header>
                    <Title>Static Singleton</Title>
                    <Shortcut>ston</Shortcut>
                    <Description>Code snippet for singleton</Description>
                    <Author>chaoming.edc</Author>
                    <SnippetTypes>
                        <SnippetType>Expansion</SnippetType>
                    </SnippetTypes>
                </Header>
                <Snippet>
                    <Declarations>
                        <Literal Editable="false">
                            <ID>classname</ID>
                            <ToolTip>Class name</ToolTip>
                            <Function>ClassName()</Function>
                            <Default>ClassNamePlaceholder</Default>
                        </Literal>
                    </Declarations>
                    <Code Language="csharp"><![CDATA[/// <summary>
            /// 静态初始化，依赖CLR实现线程安全的实例初始化
            /// </summary>
            private static readonly $classname$ instance = new $classname$();
            private $classname$() { }
            public static $classname$ Instance
            {
                get
                {
                    return instance;
                }
            }
            $end$]]>
                    </Code>
                </Snippet>
            </CodeSnippet>
        </CodeSnippets>

2. Double-Check单例

        <?xml version="1.0" encoding="utf-8" ?>
        <CodeSnippets  xmlns="http://schemas.microsoft.com/VisualStudio/2005/CodeSnippet">
            <CodeSnippet Format="1.0.0">
                <Header>
                    <Title>Double-Check Singleton</Title>
                    <Shortcut>dston</Shortcut>
                    <Description>Code snippet for singleton</Description>
                    <Author>chaoming.edc</Author>
                    <SnippetTypes>
                        <SnippetType>Expansion</SnippetType>
                    </SnippetTypes>
                </Header>
                <Snippet>
                    <Declarations>
                        <Literal Editable="false">
                            <ID>classname</ID>
                            <ToolTip>Class name</ToolTip>
                            <Function>ClassName()</Function>
                            <Default>ClassNamePlaceholder</Default>
                        </Literal>
                    </Declarations>
                    <Code Language="csharp"><![CDATA[private static object syncRoot = new object();
            private static $classname$ instance;
            private $classname$() { }

            /// <summary>
            /// Double-Check Singleton
            /// </summary>
            public static $classname$ Instance
            {
                get
                {
                    if(instance == null)
                    {
                        lock(syncRoot)
                        {
                            if(instance == null)
                            {
                                instance = new $classname$();
                            }
                        }
                    }
                    return instance;
                }
            }
            $end$]]>
                    </Code>
                </Snippet>
            </CodeSnippet>
        </CodeSnippets>

3. Nested单例

        <?xml version="1.0" encoding="utf-8" ?>
        <CodeSnippets  xmlns="http://schemas.microsoft.com/VisualStudio/2005/CodeSnippet">
            <CodeSnippet Format="1.0.0">
                <Header>
                    <Title>Nested Singleton</Title>
                    <Shortcut>nston</Shortcut>
                    <Description>Code snippet for singleton</Description>
                    <Author>chaoming.edc</Author>
                    <SnippetTypes>
                        <SnippetType>Expansion</SnippetType>
                    </SnippetTypes>
                </Header>
                <Snippet>
                    <Declarations>
                        <Literal Editable="false">
                            <ID>classname</ID>
                            <ToolTip>Class name</ToolTip>
                            <Function>ClassName()</Function>
                            <Default>ClassNamePlaceholder</Default>
                        </Literal>
                    </Declarations>
                    <Code Language="csharp"><![CDATA[private $classname$() { }
            public static $classname$ Instance
            {
                get
                {
                    return Nested.instance;
                }
            }

            private class Nested
            {
                // Explicit static constructor to tell C# compiler
                // not to mark type as before field init
                static Nested()
                {
                }

                internal static readonly $classname$ instance = new $classname$();
            }
            $end$]]>
                    </Code>
                </Snippet>
            </CodeSnippet>
        </CodeSnippets>

4. Lazy<T>单例

        <?xml version="1.0" encoding="utf-8" ?>
        <CodeSnippets  xmlns="http://schemas.microsoft.com/VisualStudio/2005/CodeSnippet">
            <CodeSnippet Format="1.0.0">
                <Header>
                    <Title>Lazy Static Singleton</Title>
                    <Shortcut>lston</Shortcut>
                    <Description>Code snippet for singleton</Description>
                    <Author>chaoming.edc</Author>
                    <SnippetTypes>
                        <SnippetType>Expansion</SnippetType>
                    </SnippetTypes>
                </Header>
                <Snippet>
                    <Declarations>
                        <Literal Editable="false">
                            <ID>classname</ID>
                            <ToolTip>Class name</ToolTip>
                            <Function>ClassName()</Function>
                            <Default>ClassNamePlaceholder</Default>
                        </Literal>
                    </Declarations>
                    <Code Language="csharp"><![CDATA[/// <summary>
            /// 静态初始化，依赖CLR实现线程安全的实例初始化，利用Lazy<T>实现懒初始化，但需要.NET4以上支持
            /// </summary>
            private static readonly Lazy<$classname$> instance = new Lazy<$classname$>(() => new $classname$());
            private $classname$() { }
            public static $classname$ Instance
            {
                get
                {
                    return instance.Value;
                }
            }
            $end$]]>
                    </Code>
                </Snippet>
            </CodeSnippet>
        </CodeSnippets>

下载链接：[https://www.dropbox.com/s/nfreaxro1jzsb80/Singleton%20Snippets.7z](https://www.dropbox.com/s/nfreaxro1jzsb80/Singleton%20Snippets.7z)