import { useEffect, useRef, useState } from 'react';
import MDEditor from '@uiw/react-md-editor';

export function MarkdownEditor() {
  const [markdown, setMarkdown] = useState('type markdown here');
  const [html, setHtml] = useState('');
  const [isPreviewMode, setIsPreviewMode] = useState(false);
  const hiddenPreviewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      setHtml(hiddenPreviewRef.current?.innerHTML ?? '');
    });

    return () => cancelAnimationFrame(frame);
  }, [markdown]);

  return (
    <div data-color-mode="light">
      <div role="toolbar" aria-label="Markdown editor controls">
        <button
          type="button"
          onClick={() => setIsPreviewMode((previous) => !previous)}
          aria-pressed={isPreviewMode}
          aria-label={isPreviewMode ? 'Switch to edit mode' : 'Switch to preview mode'}
        >
          {isPreviewMode ? 'Edit' : 'Preview'}
        </button>
      </div>

      {isPreviewMode ? (
        <MDEditor.Markdown source={markdown} />
      ) : (
        <MDEditor
          value={markdown}
          onChange={(value = '') => setMarkdown(value)}
          preview="edit"
          aria-label="Markdown editor"
        />
      )}

      <div
        ref={hiddenPreviewRef}
        aria-hidden="true"
        style={{
          position: 'absolute',
          width: 1,
          height: 1,
          overflow: 'hidden',
          clipPath: 'inset(50%)',
          whiteSpace: 'nowrap',
        }}
      >
        <MDEditor.Markdown source={markdown} />
      </div>

      <textarea
        aria-label="Rendered HTML output"
        value={html}
        readOnly
        tabIndex={-1}
        style={{ position: 'absolute', left: '-9999px' }}
      />
    </div>
  );
}

export default MarkdownEditor;
