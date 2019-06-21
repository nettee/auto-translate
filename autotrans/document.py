import markdown


def print_recursive(elem, i, indent):
    print(' ' * indent, end='')
    print('[{}]'.format(i), end='')
    if elem.text is None:
        print(elem.tag, elem.attrib)
    else:
        print(elem.tag, elem.attrib, elem.text.strip())
    for i, child in enumerate(elem):
        print_recursive(child, i, indent + 4)


class Document:

    markdown_extensions = ['markdown.extensions.fenced_code']

    def __init__(self, file):
        self.file = file
        with file.open('r') as f:
            content = f.read()
        # print(content)

        md = markdown.core.Markdown(extensions=self.markdown_extensions)
        root = self.parse(md, content)

        # print_recursive(root, 0, 0)

        codeblock = root[9]
        # print(type(codeblock), codeblock.text, codeblock.text.encode('utf-8'))

    def parse(self, md, source):
        """
        Copied and tailored from markdown.core.Markdown.convert

        arguments:

        * md: the Markdown object itself

        Originally, markdown processing takes place in five steps:

        1. A bunch of "preprocessors" munge the input text.
        2. BlockParser() parses the high-level structural elements of the
           pre-processed text into an ElementTree.
        3. A bunch of "treeprocessors" are run against the ElementTree. One
           such treeprocessor runs InlinePatterns against the ElementTree,
           detecting inline markup.
        4. Some post-processors are run against the text after the ElementTree
           has been serialized into text.
        5. The output is written to a string.

        We use the first two steps as it is, replace the processor with our own,
        and discard the last two steps.
        """

        # Fixup the source text
        if not source.strip():
            return ''  # a blank unicode string

        try:
            source = markdown.util.text_type(source)
        except UnicodeDecodeError as e:  # pragma: no cover
            # Customise error message while maintaining original trackback
            e.reason += '. -- Note: Markdown only accepts unicode input!'
            raise

        # Split into lines and run the line preprocessors.
        self.lines = source.split("\n")
        for prep in md.preprocessors:
            self.lines = prep.run(self.lines)

        # Parse the high-level elements.
        root = md.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in md.treeprocessors:
            newRoot = treeprocessor.run(root)
            if newRoot is not None:
                root = newRoot

        output = md.serializer(root)

        # Strip top-level tag, i.e. <div>
        try:
            start = output.index(
                '<%s>' % md.doc_tag) + len(md.doc_tag) + 2
            end = output.rindex('</%s>' % md.doc_tag)
            output = output[start:end].strip()
        except ValueError:  # pragma: no cover
            if output.strip().endswith('<%s />' % md.doc_tag):
                # We have an empty document
                output = ''
            else:
                # We have a serious problem
                raise ValueError('Markdown failed to strip top-level '
                                 'tags. Document=%r' % output.strip())

        # Run the text post-processors
        # In this phase the code blocks are replaced with real codes
        postprocessors = [
            # markdown.postprocessors.RawHtmlPostprocessor(md),
            # markdown.postprocessors.AndSubstitutePostprocessor(),
            # markdown.postprocessors.UnescapePostprocessor(),
        ]
        for pp in postprocessors:
            output = pp.run(output)

        print(output)

        return root
