Adding furigana to a book
=========================

The example is wildly inefficient, I wanted to know how I should do things more efficiently, so I asked:

```
❯ If I wanted to run this script but not reading lines from a terminal, instead reading an entire book from a file called book.txt, what would be 
   the most cost efficient way to do this if time isn't an issue (e.g. I'd be happy to submit a job and retrieve the results much later)?         
```

Claude response:
                                                                                                                                                  
```
⏺ The Message Batches API is exactly the right tool for this. Submit a job, come back in up to 24 hours (most batches finish within an hour), pay 
  50% of the standard price on all input and output tokens. Stack that with prompt caching and you get the cheapest path to a whole-book
  annotation.
                                                                                                                                                  
  The script:
                                                                                                                                                  
  import json     
  import time
  from pathlib import Path
  import anthropic                                                                                                                                
  from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.messages.batch_create_params import Request                                                                                
                                                                                                                                                  
  SYSTEM_PROMPT = """You are a furigana annotator..."""  # same prompt as before                                                                  
                                                                                                                                                  
  CHUNK_CHARS = 4000  # Japanese chars per request; tune to taste                                                                                 
                  
  def chunk_book(text: str, target_chars: int) -> list[str]:                                                                                      
      """Split into chunks at paragraph boundaries, never mid-sentence."""
      paragraphs = text.split("\n\n")                                                                                                             
      chunks, current = [], ""
      for p in paragraphs:                                                                                                                        
          if not p.strip():                                                                                                                       
              continue
          if len(current) + len(p) + 2 > target_chars and current:                                                                                
              chunks.append(current)
              current = p
          else:
              current = f"{current}\n\n{p}" if current else p
      if current:                                                                                                                                 
          chunks.append(current)
      return chunks                                                                                                                               
                  
  def submit(client: anthropic.Anthropic, chunks: list[str]) -> str:                                                                              
      requests = [
          Request(                                                                                                                                
              custom_id=f"chunk-{i:06d}",
              params=MessageCreateParamsNonStreaming(                                                                                             
                  model="claude-sonnet-4-6",
                  max_tokens=32000,                                                                                                               
                  thinking={"type": "adaptive"},
                  output_config={"effort": "medium"},                                                                                             
                  system=[{
                      "type": "text",                                                                                                             
                      "text": SYSTEM_PROMPT,                                                                                                      
                      "cache_control": {"type": "ephemeral"},
                  }],                                                                                                                             
                  messages=[{"role": "user", "content": chunk}],
              ),                                                                                                                                  
          )
          for i, chunk in enumerate(chunks)                                                                                                       
      ]           
      batch = client.messages.batches.create(requests=requests)
      return batch.id                                                                                                                             
   
  def collect(client: anthropic.Anthropic, batch_id: str) -> dict[str, str]:                                                                      
      while True: 
          batch = client.messages.batches.retrieve(batch_id)                                                                                      
          if batch.processing_status == "ended":
              break
          print(f"  status={batch.processing_status} "                                                                                            
                f"processing={batch.request_counts.processing} "
                f"succeeded={batch.request_counts.succeeded} "                                                                                    
                f"errored={batch.request_counts.errored}")
          time.sleep(60)                                                                                                                          
                                                                                                                                                  
      results = {}
      for r in client.messages.batches.results(batch_id):                                                                                         
          if r.result.type == "succeeded":
              text = next(b.text for b in r.result.message.content if b.type == "text")                                                           
              results[r.custom_id] = text                                                                                                         
          else:                                                                                                                                   
              print(f"  FAILED {r.custom_id}: {r.result.type}")                                                                                   
      return results                                                                                                                              
   
  def main() -> None:                                                                                                                             
      book = Path("book.txt").read_text(encoding="utf-8")
      chunks = chunk_book(book, CHUNK_CHARS)                                                                                                      
      print(f"Book: {len(book):,} chars → {len(chunks)} chunks")
                                                                                                                                                  
      client = anthropic.Anthropic()
      batch_id = submit(client, chunks)                                                                                                           
      print(f"Submitted batch {batch_id}")
      Path("batch_id.txt").write_text(batch_id)                                                                                                   
                                                                                                                                                  
      results = collect(client, batch_id)                                                                                                         
      annotated = "\n\n".join(results[f"chunk-{i:06d}"] for i in range(len(chunks)))                                                              
      Path("book.annotated.html").write_text(annotated, encoding="utf-8")                                                                         
      print(f"Wrote {len(annotated):,} chars to book.annotated.html")                                                                             
                                                                                                                                                  
  if __name__ == "__main__":                                                                                                                      
      main()      
                                                                                                                                                  
  Why this is cost-efficient:

  ┌────────────────────────────────────┬──────────────────────────────────────────────────────────┐                                               
  │            Optimization            │                          Saving                          │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────┤                                               
  │ Batches API                        │ 50% off all tokens                                       │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────┤
  │ Larger chunks (4K chars)           │ Fewer requests → less per-request system-prompt overhead │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────┤                                               
  │ Sonnet 4.6 vs Opus 4.7             │ ~40% cheaper on input, ~40% cheaper on output            │
  ├────────────────────────────────────┼──────────────────────────────────────────────────────────┤                                               
  │ (Optional) Cacheable system prompt │ ~90% off the system-prompt portion of every request      │
  └────────────────────────────────────┴──────────────────────────────────────────────────────────┘                                               
                  
  The caching gotcha to know about. Your current system prompt is ~1000 tokens — below Sonnet 4.6's 2048-token cache threshold. The cache_control 
  marker is silently a no-op. With ~250 chunks in a typical novel, you'll re-pay the system prompt cost on every chunk. If you extend the system 
  prompt past 2048 tokens (more examples is the natural way — gemination cases, rendaku cases, heteronym cases), the marker engages, the first    
  chunk pays a small write premium, and the remaining 249 cost ~10% on the cached portion. That's a ~85–90% saving on the system-prompt fraction
  of every request, on top of the 50% batch discount. For a book this is the difference between cents and dollars; for a series of books it adds
  up.

  Order matters: stable prefix first. Caching is a prefix match — if even one byte before the breakpoint varies between requests, the cache       
  misses. The script above is fine because every request has identical system. Don't interpolate per-chunk metadata into the system prompt.
                                                                                                                                                  
  One robustness note: validate the preservation invariant. Once you have annotated output, strip every <rt>...</rt> and compare to the original  
  chunk byte-for-byte. The model is overwhelmingly faithful, but on long inputs occasional drift happens (skipped sentence, re-formatted
  whitespace). A quick check after collection saves a lot of debugging:                                                                           
                  
  import re
  strip_rt = re.compile(r"<ruby>([^<]*?)<rt>[^<]*</rt></ruby>")
  recovered = strip_rt.sub(r"\1", annotated_chunk)                                                                                                
  assert recovered == original_chunk, f"drift in chunk {i}"                                                                                       
                                                                                                                                                  
  If a chunk fails the round-trip, resubmit just that one in a small follow-up batch.                                                             
                                                                                                                                                  
  A heads-up on cost vs quality. Sonnet 4.6 will get the bulk right but is meaningfully weaker than Opus 4.7 on heteronym disambiguation in       
  literary text. For a book with classical or theatrical content (where you've seen 上手, 一日, 何, 角 disambiguation matter), Opus 4.7 batched is
   still ~50% off list price and gives you a noticeably better result. Worth the bump if accuracy matters more than absolute floor cost.          
                  
  One more option, if you genuinely don't care about latency at all and want the absolute floor: Haiku 4.5 batched. ~70% cheaper input than Sonnet
   4.6, ~70% cheaper output. Quality drops noticeably on hard heteronyms and counter-compound gemination, but for a casual reading aid it's
  defensible. I'd run a few representative chunks through Haiku first to see whether the failures are tolerable for your use case before          
  committing to a whole book.
```

Note that earlier, it has said:

```
  For your script as written: the system prompt is too short to trigger caching at all, so every line costs the full ~800–1000 tokens of input
  regardless of the marker. At Opus 4.7's pricing ($5/1M input), that's about $0.005 per request — small enough that it likely doesn't matter for
  personal use.
```

This _seems_ to imply that repeating the system prompt, i.e. not bothering with caching discussed above, would only add 5 cents per 1000 requests even for Opus.

And above, it mentions sanity checking the input can be recovered from the output, i.e. strip the ruby tags, and earlier it suggested more sanity checking, this time of the ruby tags themselves (and their content):

```
  - Validation is cheap and worth doing. A regex <rt>([^<]+)</rt> lets you pull every reading; a separate kana-only check (every <rt> content
  matches ^[ぁ-ゟー]+$) catches the case where the model accidentally puts kanji or English in the reading.
```
