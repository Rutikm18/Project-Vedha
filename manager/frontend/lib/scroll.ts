/** Scroll `child` to the top of `container` — and nothing else.
 *
 * `element.scrollIntoView()` also scrolls every scrollable ancestor, which nudged the
 * whole page when a reply arrived inside the chat panel. This moves only the chat. */
export function scrollChildToTop(container: HTMLElement, child: HTMLElement, behavior: ScrollBehavior = "smooth", gap = 12) {
  const top = child.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop - gap;
  container.scrollTo({ top: Math.max(0, top), behavior });
}

/** Scroll `container` to its end. */
export function scrollToEnd(container: HTMLElement, behavior: ScrollBehavior = "smooth") {
  container.scrollTo({ top: container.scrollHeight, behavior });
}
