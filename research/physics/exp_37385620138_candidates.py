#!/usr/bin/env python3
"""
EXP-PHYSICS-37385620138 — candidate universe (prereg s5.1).

prereg s5.1 permits the union of three sources:
    "Tranco top 1M + Common Crawl index + manual curation list"

This executor implements the THIRD arm only.  Tranco and the Common Crawl index
are external bulk indexes that are not present in this repository and cannot be
re-derived from any frozen artifact, so reproducing them is not possible here.
The manual-curation arm is explicitly one of the three frozen sources, so using
it does not change the frozen design; it does mean the frozen "Tranco / Common
Crawl" arms are unrepresented, which is recorded in validity_notes.

Admission is still governed entirely by the frozen variation-coverage screen
(prereg s5.2), so the curation arm only affects which candidates enter the screen,
never which sites are admitted.

The universe is materialised in a deterministic order derived from
master_seed = int(request_hash[:8], 16) (prereg s5.1), so the same request digest
always yields the same screen order.
"""

from __future__ import annotations

# (host, [document URLs])  -- public, credential-free, HTML documents.
# Four documents where available so that the universe approaches the frozen
# "200 candidate (site, document) pairs across >= 50 eTLD+1" target.
SITE_DOCUMENTS: list[tuple[str, list[str]]] = [
    ("en.wikipedia.org", [
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/HTTP",
        "https://en.wikipedia.org/wiki/Cache-control",
        "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol",
    ]),
    ("developer.mozilla.org", [
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP",
        "https://developer.mozilla.org/en-US/docs/Web/Performance",
        "https://developer.mozilla.org/en-US/docs/Web/CSS",
    ]),
    ("docs.python.org", [
        "https://docs.python.org/3/tutorial/introduction.html",
        "https://docs.python.org/3/library/json.html",
        "https://docs.python.org/3/library/http.client.html",
        "https://docs.python.org/3/library/urllib.request.html",
    ]),
    ("nodejs.org", [
        "https://nodejs.org/en/docs/getting-started/introduction-to-nodejs",
        "https://nodejs.org/en/docs/guides",
        "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs",
    ]),
    ("www.w3.org", [
        "https://www.w3.org/TR/HTML52/",
        "https://www.w3.org/TR/CSS21/",
        "https://www.w3.org/TR/2011/WD-html5-20111213/",
        "https://www.w3.org/TR/WebCryptoAPI/",
    ]),
    ("www.rfc-editor.org", [
        "https://www.rfc-editor.org/rfc/rfc9110.html",
        "https://www.rfc-editor.org/rfc/rfc9111.html",
        "https://www.rfc-editor.org/rfc/rfc7234.html",
        "https://www.rfc-editor.org/rfc/rfc9110.txt",
    ]),
    ("datatracker.ietf.org", [
        "https://datatracker.ietf.org/doc/html/rfc9110",
        "https://datatracker.ietf.org/doc/html/rfc9111",
        "https://datatracker.ietf.org/doc/html/rfc7231",
    ]),
    ("www.ietf.org", [
        "https://www.ietf.org/",
        "https://www.ietf.org/about/introduction/",
    ]),
    ("www.gnu.org", [
        "https://www.gnu.org/manual/glibc/html_mono/glibc.html",
        "https://www.gnu.org/manual/libc/html_node/Contents.html",
        "https://www.gnu.org/philosophy/free-sw.html",
        "https://www.gnu.org/licenses/gpl-faq.html",
    ]),
    ("www.kernel.org", [
        "https://www.kernel.org/doc/html/latest/admin-guide/index.html",
        "https://www.kernel.org/doc/html/latest/networking/index.html",
        "https://www.kernel.org/doc/html/latest/filesystems/index.html",
        "https://www.kernel.org/doc/html/latest/process/index.html",
    ]),
    ("docs.kernel.org", [
        "https://docs.kernel.org/networking/index.html",
        "https://docs.kernel.org/filesystems/index.html",
        "https://docs.kernel.org/admin-guide/index.html",
    ]),
    ("www.apache.org", [
        "https://www.apache.org/httpd/2.4/doc/mod/mod_cache.html",
        "https://www.apache.org/httpd/2.4/docs/2.4-en/",
        "https://www.apache.org/tomcat/",
    ]),
    ("www.postgresql.org", [
        "https://www.postgresql.org/docs/current/static/httpresource.html",
        "https://www.postgresql.org/docs/current/static/caching.html",
        "https://www.postgresql.org/docs/current/mtts.html",
    ]),
    ("dev.mysql.com", [
        "https://dev.mysql.com/doc/refman/8.0/en/caching.html",
        "https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html",
        "https://dev.mysql.com/doc/refman/8.4/en/caching.html",
    ]),
    ("redis.io", [
        "https://redis.io/docs/latest/operate/rs/databases/",
        "https://redis.io/docs/latest/develop/clients/",
        "https://redis.io/docs/latest/operate/oss_and_stack/",
    ]),
    ("www.elastic.co", [
        "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html",
        "https://www.elastic.co/guide/en/kibana/current/index.html",
        "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html",
    ]),
    ("docs.docker.com", [
        "https://docs.docker.com/engine/containers/",
        "https://docs.docker.com/compose/intro/",
        "https://docs.docker.com/build/",
        "https://docs.docker.com/engine/storage/",
    ]),
    ("docs.aws.amazon.com", [
        "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
        "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
        "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html",
    ]),
    ("aws.amazon.com", [
        "https://aws.amazon.com/blogs/compute/",
        "https://aws.amazon.com/blogs/database/",
    ]),
    ("cloud.google.com", [
        "https://cloud.google.com/compute/docs/instances/overview",
        "https://cloud.google.com/storage/docs/overview",
        "https://cloud.google.com/functions/docs/overview",
    ]),
    ("research.google", [
        "https://research.google/blog/",
        "https://research.google/pubs/",
    ]),
    ("developer.android.com", [
        "https://developer.android.com/guide/components/activities/activity-lifecycle",
        "https://developer.android.com/training/basics/activity-lifecycle",
        "https://developer.android.com/develop/ui/views/layout/declaring-layout",
    ]),
    ("developer.apple.com", [
        "https://developer.apple.com/documentation/",
        "https://developer.apple.com/library/archive/documentation/",
        "https://developer.apple.com/safety/",
    ]),
    ("learn.microsoft.com", [
        "https://learn.microsoft.com/en-us/azure/azure-fundamentals/",
        "https://learn.microsoft.com/en-us/azure/virtual-machines/",
    ]),
    ("docs.microsoft.com", [
        "https://docs.microsoft.com/en-us/azure/architecture/",
    ]),
    ("www.microsoft.com", [
        "https://www.microsoft.com/en-us/research/blog/",
        "https://www.microsoft.com/en-us/research/publications/",
    ]),
    ("docs.github.com", [
        "https://docs.github.com/en/get-started",
        "https://docs.github.com/en/actions",
        "https://docs.github.com/en/rest",
        "https://docs.github.com/en/rest/using-the-rest-api",
    ]),
    ("support.github.com", [
        "https://support.github.com/contact",
        "https://support.github.com/articles/about-github",
    ]),
    ("developer.hashicorp.com", [
        "https://developer.hashicorp.com/terraform/docs",
        "https://developer.hashicorp.com/vault/docs",
        "https://developer.hashicorp.com/nomad/docs",
    ]),
    ("www.terraform.io", [
        "https://www.terraform.io/docs/language/index.html",
        "https://www.terraform.io/docs/language/expressions/index.html",
    ]),
    ("www.rust-lang.org", [
        "https://www.rust-lang.org/learn",
        "https://www.rust-lang.org/tools/install",
        "https://www.rust-lang.org/production/usage",
    ]),
    ("doc.rust-lang.org", [
        "https://doc.rust-lang.org/book/ch01-00-getting-started.html",
        "https://doc.rust-lang.org/std/collections/index.html",
        "https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html",
    ]),
    ("crates.io", [
        "https://crates.io/crates/serde",
        "https://crates.io/crates/tokio",
    ]),
    ("go.dev", [
        "https://go.dev/ref/spec",
        "https://go.dev/doc/tutorial/",
        "https://go.dev/doc/effective_go.html",
        "https://go.dev/doc/faq",
    ]),
    ("pkg.go.dev", [
        "https://pkg.go.dev/net/http",
        "https://pkg.go.dev/context",
    ]),
    ("www.typescriptlang.org", [
        "https://www.typescriptlang.org/docs/handbook/intro.html",
        "https://www.typescriptlang.org/docs/",
        "https://www.typescriptlang.org/play",
    ]),
    ("babeljs.io", [
        "https://babeljs.io/docs/",
        "https://babeljs.io/docs/usage/",
    ]),
    ("react.dev", [
        "https://react.dev/learn",
        "https://react.dev/reference/react/useState",
        "https://react.dev/reference/react-dom/client/createRoot",
    ]),
    ("vuejs.org", [
        "https://vuejs.org/guide/introduction.html",
        "https://vuejs.org/api/",
        "https://vuejs.org/guide/introduction.html#setup",
    ]),
    ("angular.dev", [
        "https://angular.dev/guide/components",
        "https://angular.dev/guide/http",
    ]),
    ("svelte.dev", [
        "https://svelte.dev/docs/kit",
        "https://svelte.dev/docs",
    ]),
    ("nextjs.org", [
        "https://nextjs.org/docs/app",
        "https://nextjs.org/docs/pages/building-your-application/routing",
    ]),
    ("www.tailwindcss.com", [
        "https://www.tailwindcss.com/docs",
        "https://www.tailwindcss.com/docs/installation",
    ]),
    ("getbootstrap.com", [
        "https://getbootstrap.com/docs/5.3/getting-started/introduction/",
        "https://getbootstrap.com/docs/5.3/layout/grid/",
    ]),
    ("jquery.com", [
        "https://jquery.com/api/",
        "https://jquery.com/download/",
        "https://api.jquery.com/",
    ]),
    ("d3js.org", [
        "https://d3js.org/getting-started",
        "https://d3js.org/examples/",
    ]),
    ("www.sqlite.org", [
        "https://www.sqlite.org/lang.html",
        "https://www.sqlite.org/docs.html",
        "https://www.sqlite.org/fts5.html",
        "https://www.sqlite.org/wal.html",
    ]),
    ("www.debian.org", [
        "https://www.debian.org/doc/manuals/",
        "https://www.debian.org/intro",
        "https://www.debian.org/users/",
    ]),
    ("ubuntu.com", [
        "https://ubuntu.com/server/docs",
        "https://ubuntu.com/tutorials",
    ]),
    ("wiki.archlinux.org", [
        "https://wiki.archlinux.org/title/Main_page",
        "https://wiki.archlinux.org/title/System_maintenance",
        "https://wiki.archlinux.org/title/List_of_packages",
    ]),
    ("wiki.gentoo.org", [
        "https://wiki.gentoo.org/wiki/Introduction",
        "https://wiki.gentoo.org/wiki/Getting_started",
    ]),
    ("man7.org", [
        "https://man7.org/linux/man-pages/man7/http.7.html",
        "https://man7.org/linux/man-pages/man1/curl.1.html",
        "https://man7.org/linux/man-pages/man1/git.1.html",
    ]),
    ("html.spec.whatwg.org", [
        "https://html.spec.whatwg.org/multipage/",
        "https://html.spec.whatwg.org/multipage/browsers.html",
    ]),
    ("dom.spec.whatwg.org", [
        "https://dom.spec.whatwg.org/",
    ]),
    ("tc39.es", [
        "https://tc39.es/ecma262/multipage/",
        "https://tc39.es/ecma262/",
    ]),
    ("www.nasa.gov", [
        "https://www.nasa.gov/",
        "https://www.nasa.gov/missions/",
    ]),
    ("www.noaa.gov", [
        "https://www.noaa.gov/",
    ]),
    ("www.gutenberg.org", [
        "https://www.gutenberg.org/ebooks/",
        "https://www.gutenberg.org/policy/",
    ]),
    ("en.wikisource.org", [
        "https://en.wikisource.org/wiki/Main_Page",
    ]),
    ("en.wiktionary.org", [
        "https://en.wiktionary.org/wiki/Main_Page",
    ]),
    ("lwn.net", [
        "https://lwn.net/Articles/",
    ]),
    ("www.smashingmagazine.com", [
        "https://www.smashingmagazine.com/2023/09/",
    ]),
    ("css-tricks.com", [
        "https://css-tricks.com/almanac/",
        "https://css-tricks.com/snippets/css/",
    ]),
    ("openstax.org", [
        "https://openstax.org/books/",
    ]),
    ("www.ncbi.nlm.nih.gov", [
        "https://www.ncbi.nlm.nih.gov/books/",
    ]),
    ("europepmc.org", [
        "https://europepmc.org/",
    ]),
    ("arxiv.org", [
        "https://arxiv.org/list/cs.AI/recent",
        "https://arxiv.org/abs/1706.03762",
    ]),
    ("sourceware.org", [
        "https://sourceware.org/git/",
    ]),
    ("www.erlang.org", [
        "https://www.erlang.org/doc/man/",
        "https://www.erlang.org/docs/",
    ]),
    ("www.scala-lang.org", [
        "https://www.scala-lang.org/documentation/",
    ]),
    ("clojure.org", [
        "https://clojure.org/guides",
        "https://clojure.org/learn",
    ]),
    ("pypi.org", [
        "https://pypi.org/project/requests/",
        "https://pypi.org/project/flask/",
    ]),
    ("rubygems.org", [
        "https://rubygems.org/gems/rails",
    ]),
    ("packagist.org", [
        "https://packagist.org/packages/",
    ]),
    ("npmjs.com", [
        "https://www.npmjs.com/package/lodash",
    ]),
    ("nginx.org", [
        "https://nginx.org/en/docs/",
        "https://nginx.org/en/docs/http/",
    ]),
    ("www.perl.org", [
        "https://www.perl.org/docs/",
    ]),
    ("www.nist.gov", [
        "https://www.nist.gov/pml",
    ]),
    ("csrc.nist.gov", [
        "https://csrc.nist.gov/pubs/sp/800/38/3/final",
    ]),
    ("www.iso.org", [
        "https://www.iso.org/standards.html",
    ]),
    ("www.unicode.org", [
        "https://www.unicode.org/versions/",
        "https://www.unicode.org/charts/",
    ]),
    ("blog.python.org", [
        "https://blog.python.org/",
    ]),
    ("www.python.org", [
        "https://www.python.org/doc/",
    ]),
]


def candidate_pairs() -> list[dict]:
    """Deterministically ordered (site, document) candidate pairs."""
    out = []
    for host, docs in SITE_DOCUMENTS:
        for doc in docs:
            out.append({"host": host, "document_url": doc})
    return out