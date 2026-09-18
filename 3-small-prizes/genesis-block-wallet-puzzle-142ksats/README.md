# Genesis Block Wallet Puzzle (231,501 sats, [OPEN])

On 2026-08-22 an anonymous author published a 252-byte OP_RETURN message in block 963,629:
a Bitcoin wallet generated only from data in Satoshi's genesis block, "extremely low"
entropy, nothing backed up. The prize sits in the first output of that same transaction, a
P2WSH address, and it grows every time someone pays for a hint: the author answers questions
on chain and relays every payment into the escrow. Eleven author messages so far fix the
shape of the lock: a 2-of-2 multisig, both keys from one genesis field, no hash, a field you
can read in The Times, the BIP48 level order, and since 2026-09-11 the root itself: a
12-word BIP39 mnemonic whose entropy is genesis data, with a passphrase, and a genesis value
as the BIP48 account number. Five further answers between 2026-09-14 and 2026-09-17 name the
passphrase as the name of whoever received the first transaction, in a format the author
says must be brute-forced, and fix the entropy as a 128-bit digest rather than raw genesis
bytes. The oracle is exact and offline. Four passes have now been run and none matched:
611,008 keys on 2026-08-29, the raw-window model on 2026-09-12, and the digest model on
2026-09-17.

## At a glance

| | |
|---|---|
| Author | anonymous, on-chain only (every message is an OP_RETURN sent to the escrow) |
| Published | 2026-08-22, OP_RETURN in block 963,629 ([transaction](https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77)) |
| Prize | 231,501 sats (about $146 at BTC = $63,000, the 2026-08-16 snapshot); 229,724 sats earlier the same day, 168,779 on 2026-09-12, 142,779 on 2026-08-29, growing with each paid question |
| Chain | bitcoin |
| Escrow | `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj` ([explorer](https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj)) |
| Last on-chain check | 2026-09-18: funded and unspent, 38 confirmed outputs, 0 spent, nothing pending, confirmed on mempool.space |
| Status | OPEN |
| Puzzle type | multisig, raw-private-key |
| Target format | P2WSH (v0), witness script `OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG`, both keys derived from one genesis-block field |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the BIP-173 P2WSH vector and a real 2-of-2 spent in block 963,629) |
| What remains | insight: which part of the genesis block is hashed into the 128-bit entropy. A 10,000-sat question asking for the category of that part was refused on 2026-09-18, at the price that bought two informative answers in September; the author answers about the form of the input and not about the input |
| Series | none |

## The puzzle as published

The author has no website, no forum thread and no handle. Everything is in OP_RETURN outputs
of transactions paid to the escrow, readable by anyone. Verbatim texts with txids are in
[clues/author-posts.md](clues/author-posts.md); the full ledger of the 18 transactions is in
[data/on-chain-dialogue.json](data/on-chain-dialogue.json).

Announcement, 2026-08-22 19:45:38 UTC, block 963,629,
`b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77`:

> "I made a Bitcoin puzzle using information contained in the genesis block created by
> Satoshi to generate the wallet. The entropy is extremely low. I didn't even need to back
> anything up. Everything I needed was already in the genesis block. Good luck!"

Hint channel, 2026-08-23 01:51 UTC:

> "If you have a question, you can include it with a transaction sent directly to this
> address, and I will reply with a hint. Larger payments receive better hints. Dust
> transactions will be ignored."

Answers given so far, in order (the questions are in the clues file):

| Date (UTC) | Author's answer |
|---|---|
| 2026-08-23 15:43 | "The witness script is a multisig." |
| 2026-08-23 21:08 | "Two keys, both required. The rest is for you to derive." |
| 2026-08-24 07:13 | "Yes, both keys use the same Genesis field, and there is no hash." |
| 2026-08-24 14:32 | "Both keys are derived independently from Genesis." |
| 2026-08-24 21:35 | "The Genesis Block is public. Which part of it matters is for you to discover." |
| 2026-08-28 23:15 | "Solve it to find out. Maybe both. If you can't check the Genesis block, you can also use The Times newspaper!" (asked: "Prize Address? Genesis field 32 bytes or smaller?") |
| 2026-08-28 23:50 | `Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type` (asked: "Can you give any hint about derivation offset/rule?") |
| 2026-09-06 19:41 | "I can't give hints without a question. Low-value transactions get bad hints; dust will be ignored." (a player had sent 1,000 sats with "give another hint") |
| 2026-09-10 21:33 | "root = the master key derived from the BIP39 seed; genesis_data = some data from the genesis block used as the BIP48 account number." (asked, 10,000 sats: "Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account?") |
| 2026-09-11 23:26 | "BIP39: 12 words; Passphrase: Y; Entropy: The data needed to solve it is publicly available in the genesis block." (asked, 10,000 sats: "BIP39 entropy: genesis bytes/puzzle text/img/other? words 12/24? passphrase Y/N?") |
| 2026-09-14 16:15 | "Passphrase: Who received the first transaction? That's all I've got to say. What built the wallet are the tools that support BIPs 32, 39, and 48." (asked, 10,000 sats: "Passphrase: genesis data or your own word? How long? What built the wallet?") |
| 2026-09-15 03:19 | "No, the passphrase is a name. The entropy isn't the raw 16 bytes." (asked, 4,500 sats: "Passphrase sha256 first 8 hex? Entropy: raw 16B slice of Times or sha256?") |
| 2026-09-15 15:22 | "Perhaps... but figuring that out is part of the puzzle. The 12 words were generated from entropy." (answers two questions: whether both cosigners share the words and the passphrase, 10,000 sats, and whether the words were generated or chosen, 5,000 sats) |
| 2026-09-16 12:40 | "It's a 128-bit digest." (asked, 5,000 sats: "Is the 128-bit entropy a zero-padded number, a digest, or neither?") |
| 2026-09-17 08:02 | "Passphrase: You'll have to discover the fmt through brute force. The key question greatly narrows the search space." (asked, 4,000 sats: "Passphrase fmt: first/full/middle name? spaced/joined? lower/UPPER/Capitalized?") |
| 2026-09-17 23:22 | "The genesis block data can be viewed in binary, hex, decimal, or ASCII. If you figure out which part is being used as the entropy, just try all four forms." and "Want a valuable hint? Send 50k sats and I'll reveal the public keys for this address." (asked, 3,000 sats: "Digest input: typed text, raw block bytes, a file, or something else?") |
| 2026-09-18 16:45 | "Some part of the genesis block. The hints are meant to clarify the map, not hand you the route." (asked, 10,000 sats: "Is the hashed part a header field, the coinbase text, or the whole block?") |

The corpus is the genesis block itself, 285 bytes, public since 2009-01-03
([data/genesis-block.hex](data/genesis-block.hex)):

| Field | Value | Size |
|---|---|---|
| version | 1 | 4 bytes |
| previous block hash | 32 zero bytes | 32 bytes |
| merkle root (also the coinbase txid) | `4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b` | 32 bytes |
| time | 1231006505 (2009-01-03 18:15:05 UTC) | 4 bytes |
| bits | 486604799 (`0x1d00ffff`) | 4 bytes |
| nonce | 2083236893 (`0x7c2bac1d`) | 4 bytes |
| block hash | `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f` | 32 bytes |
| coinbase scriptSig | `04ffff001d0104` + `45` + text | 77 bytes |
| coinbase text | `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks` | 69 bytes |
| the newspaper's own headline | `Chancellor on brink of second bailout for banks` | 47 bytes |
| coinbase output public key | `04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f` | 65 bytes |

## What is understood

### Mechanism

The escrow is a native P2WSH output: the address encodes `sha256(witness script)`. The author
states the witness script is a multisig with two keys, both required, so the script is
`OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG` (71 bytes with compressed keys). The unknown is
the pair of keys and their order in the script (two cases, both checked by the oracle).

Reading of the hints, in the order they constrain the search:

1. "You can also use The Times newspaper" points at the one genesis field a newspaper
   contains: the coinbase text. Its first 32 bytes are exactly
   `The Times 03/Jan/2009 Chancellor`, the size of a private key, which fits "Maybe both"
   as an answer to "32 bytes or smaller": likely one key on 32 bytes, the other on fewer.
2. "root -> multisig -> mainnet -> genesis_data -> script_type" is, word for word, the level
   order of BIP48: `m / 48' / 0' / account' / script_type'`, with a genesis value in the
   account slot. The nonce (2083236893), the timestamp and the bits value all fit under
   2^31, so all three are valid hardened indexes. Script type 2' is native P2WSH.
3. "Same field", "no hash", "derived independently": two roots built from the same text
   without an explicit SHA-256 step (raw bytes, a BIP32 seed, or BIP39 entropy), then the
   same BIP48 path; or one root and two accounts.
4. Since 2026-09-10 and 2026-09-11 the root is named: "root" is the BIP32 master key of a
   12-word BIP39 mnemonic, the mnemonic has a passphrase, its entropy is data from the
   genesis block, and "genesis_data" is a genesis value used as the BIP48 account number.
   A 12-word mnemonic carries 128 bits of entropy. Passes 1 and 2 did not cover a non-empty
   passphrase, so their negatives do not touch this model.
5. The five answers of 2026-09-14 to 2026-09-17 close two of the three unknowns and open
   one. The entropy is "a 128-bit digest" and explicitly "isn't the raw 16 bytes", which
   retires the raw-window reading that pass 3 tested: the 16 bytes are the output of a hash
   over some genesis input, not a slice of the block. The passphrase "is a name", the name
   of "who received the first transaction", which reads either as Hal Finney, the recipient
   of the first Bitcoin payment in block 170, or as Satoshi Nakamoto, who received the
   coinbase of the genesis block itself; the author says its format has to be found by brute
   force. The words "were generated from entropy", so the mnemonic is a standard BIP39
   encoding of that digest, and the wallet was built with "the tools that support BIPs 32,
   39, and 48", which is the ordinary multisig tooling. Whether both cosigners share the
   words and the passphrase is answered "Perhaps", so both the one-seed and the two-seed
   readings stay open. What is not stated is which input is hashed; a question asking
   exactly that (typed text, raw block bytes, a file, or something else) is on chain since
   2026-09-17 10:44 and unanswered.
6. The answer to that question, confirmed in block 967,477 on 2026-09-17 23:22 UTC, is the
   first statement about how the input is written rather than about which part it is: the
   genesis data "can be viewed in binary, hex, decimal, or ASCII", and a solver who works out
   which part carries the entropy should "just try all four forms". The author declines to name
   the part, and prices the escrow's two public keys at 50,000 sats. Knowing the public keys
   would remove the pairing step from a search but not the derivation, which is the larger half
   of the cost here, so it buys roughly a factor of two and no information about the input.

### Derivation and oracle

```
python3 tools/oracle.py --selftest              # must print SELFTEST OK
python3 tools/oracle.py <keyA hex> <keyB hex>   # 32-byte private keys or 33/65-byte public keys
python3 tools/oracle.py --stdin                 # one "keyA keyB" pair per line
```

The oracle rebuilds the 2-of-2 script in both key orders, hashes it, and compares all 32
bytes with the published witness program
`4dae67a9872f1402109f9670276afc2c0758f895aafddcd089795771b7964833`. No network, no false
positive. Measured on one CPU core: about 1,200,000 pairs/s once public keys exist, about
37,000 private-to-public derivations/s in Python.

### Certified against

1. The BIP-173 test vector for a P2WSH program
   (`1863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262` to
   `bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3`).
2. A real 2-of-2 P2WSH spent in the same block as the announcement, transaction
   `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`, input 0: the two
   public keys revealed in its witness, rebuilt into the script, hash to the address of the
   output it spends, `bc1q6vpcc5vdrg0dh0k4edkuvamvn27mwr4crxgl94yva9v9z240vysqr89ddy`.
3. Private key 1 derives the generator point, compressed and uncompressed.
4. Negative control: that revealed pair does not match the escrow.

### Established facts

1. The escrow holds 229,724 sats in 37 unspent confirmed outputs as of 2026-09-17, checked on
   mempool.space, with one further 1,855-sat output unconfirmed (168,779 sats in 24 outputs on
   2026-09-12, 142,779 sats in 18 outputs on 2026-08-29). The first funding (20,000 sats) confirmed in block
   963,517 on 2026-08-22 02:45 UTC, 17 hours before the announcement.
2. Every payment sent with a question ends up in the escrow. Four questions were paid
   directly to the author's change addresses (12,909, 32,357, 6,465 and 12,963 sats); the
   author re-posted each question to the escrow with the same amount minus fees, then
   posted the answer. So the jackpot is the sum of all hint payments plus the author's
   own 30,000 sats. Traced from the transaction inputs in `data/on-chain-dialogue.json`.
3. The author uses a fresh P2WPKH change address for every message and keeps a separate
   1,000,000 sats output untouched (`bc1qw8uecdjvuedtkg4s2kku4s2ak9r2cm59khclfr`, funded
   2026-08-22 from the same source as the escrow). Response time to a paid question was
   between 1 and 10 hours in every case so far.
4. Only two wallets have asked questions: one asked 5 questions on 2026-08-23 and
   2026-08-24 (about 77,000 sats paid in total), the other asked 3 on 2026-08-28. The
   first one had split its coins into 5 equal outputs of 66,020 sats on 2026-08-06, 16
   days before the puzzle existed. I record this as an observation only.
5. The two 2026-08-28 answers ("The Times newspaper", the derivation rule) are absent from
   every press article I found; the articles cover the announcement and the first two
   answers, and report the jackpot at 125,779 sats, its value on 2026-08-24.
6. The word "genesis_data" sits exactly where BIP48 puts the account index; the nonce is
   the only genesis integer that lands under 2^31 by chance (time and bits do so by
   construction).
7. The literal readings of hints 7 and 8 do not produce the keys: 447,916 distinct public
   keys built from the coinbase text and the other genesis fields (raw windows, BIP32 seeds
   and BIP39 entropy along 214 paths including every BIP48 path with a genesis integer as
   account), paired every way, give 0 match against the escrow, with the witness pair
   re-found at head, middle and tail. 2.0e11 ordered pairs in 103 s on one RTX 5080,
   2026-08-29 (`analysis/tested.md`). The two 2026-08-28 hints therefore describe a
   construction with at least one step I have not modeled, most likely how "root" is built.
8. The library-specific root constructions do not produce the keys either: hashed roots
   (SHA-256, double SHA-256, hash160, SHA-512 of the text as key, seed or entropy), a raw
   64-byte extended key cut from the text, and a raw key with a zero chain code, along the
   same 214 paths, add 165,064 keys; the union of 611,008 keys paired every way gives 0
   match, witnesses re-found, 3.7e11 ordered pairs in 89 s, 2026-08-29. "root" is therefore
   not any standard function of the coinbase text on these paths.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md), including the exact list of texts,
windows, readings and derivation paths. Reproduce with `tools/candidates.py --write --pass 2`
(about 17 s on 22 cores) and `engines/p2wsh_2of2_pairs` (about 90 s on one RTX 5080), then
`tools/candidates.py --verify` on the hits file.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Pass 1, families A to D: literal readings of hints 7 and 8 (raw keys, BIP32 seeds, BIP39 entropy from the coinbase text and the other fields, 214 paths), every ordered pair | 447,916 keys, 200,634,118,084 ordered pairs | CPU key generation (`tools/candidates.py`), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`), exact 32-byte compare, every hit re-derived on CPU | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-08-29 |
| Pass 2, A to D plus E (hashed roots), F (raw 64-byte extended key from the text), G (raw key with zero chain code), same 214 paths, every ordered pair of the union | 611,008 keys, 373,338,108,196 ordered pairs | same pipeline, `tools/candidates.py --pass 2` | 0 match | yes: same witness protocol, 9 of 9 re-found, `exhausted=yes` | 2026-08-29 |
| Six further constructions by @BorisLoveDev (PR #21): the texts directly as BIP39 sentences, the newspaper date as an integer seed, a date-prefix mnemonic, text bytes as derivation-path indices, zero roots, and 15 hardening patterns over m/48'/0'/account/script | about 42 million new ordered pairs across the six families (1,648,656 + 26,378,496 + 2,060,820 + 576 + 732,736 + 11,150,784) | CPU pairing on the same 2-of-2 program, exact 32-byte compare | 0 match | yes: revealed pair at head, middle and tail; I replayed all six locally with identical counts | 2026-09-05 |
| Pass 3, the September model (2026-09-12): 12-word BIP39 mnemonic whose entropy is a 16-byte window of genesis data (every window of the raw 285-byte block, of the merkle root and block hash in both byte orders, of the coinbase text, headline, scriptSig, header and coinbase public key, plus the header integers zero-padded and as decimal strings: 329 entropies), 53 passphrases (empty as control, the coinbase text, the headline, The Times, Satoshi, genesis, bitcoin, the header integers, the hashes in hex and a dozen short words from the author's messages), BIP48 `m/48'/0'/a'/s'` with a in {0, 1, 2, 3, 50, 2009, 285, bits, time, nonce} and s in {0', 1', 2'}, suffix empty, /0/0 or /0/1; every ordered pair | 1,569,330 keys, 2.463e12 ordered pairs | CPU BIP39/BIP32 generation (25 s on 22 cores), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`, 4.18e9 pairs/s, 589 s), exact 32-byte compare | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-09-12 |
| Pass 4 wave 1, the digest model (2026-09-17): entropy = a 128-bit digest of genesis data (18 digest readings over 73 genesis inputs, 1,278 distinct entropies), 12-word mnemonic, passphrase = one of 47 name formats for Hal Finney, Harold Finney and Satoshi Nakamoto, BIP48 with 13 genesis accounts and script types 0'/1'/2', suffix empty, /0/0, /0/1 or /1/0; both keys from the same seed, every ordered pair inside the seed | 60,066 seeds, 9,370,296 keys, 1,452,484,146 ordered pairs | CPU generation and pairing (`tools/check_digest_model.py --wave 1`), exact 32-byte compare | 0 match | yes: revealed pair in the first, middle and last entropy group, 141 of 141 re-found | 2026-09-17 |
| Pass 4 wave 2 (2026-09-17): the same entropies and passphrases, two cosigners taken from two different digests at the same path under the same passphrase, 65 paths | 3,904,290 keys, 4,986,775,560 ordered pairs | same pipeline, `--wave 2` | 0 match | yes: revealed pair at the first, middle and last passphrase, 195 of 195 re-found | 2026-09-17 |
| Pass 4 wave 3 (2026-09-17): 300 typed forms of the coinbase text, the headline and the date line (case, spacing, trailing newline, CRLF, period, quotes, eight date spellings, the block as a hex file) under 16 digest readings, 4,800 entropies, 137 name formats, 36 paths; pairs two paths under one seed and two name formats under one entropy | 4,800 entropies, 1,591,661,238 ordered pairs | same pipeline, `--wave 3` | 0 match | yes: revealed pair in the first, middle and last entropy group, 3 of 3 re-found | 2026-09-17 |
| Pass 4 wave 4, the four forms (2026-09-17): 25 genesis parts (the header fields in both byte orders, the block, the header, the coinbase transaction, the texts, the public key and its coordinates, the truncated hashes) each rendered in 11 ways covering the author's four views (raw bytes, lower and upper-case hex, the decimal value, the bit string plain, stripped and byte-spaced, the latin-1 and dotted ASCII views, the per-byte decimal lists), 4,284 entropies, 47 name formats, 52 paths; pairs inside one seed and across two entropies at the 13 native-P2WSH accounts | 4,284 entropies, 11,744,847,956 ordered pairs | CPU generation and pairing, `tools/check_digest_model.py --wave 4`, 8 processes, exact 32-byte compare | 0 match | yes: revealed pair inserted in the first, middle and last entropy group and in the cross pass, 4 of 4 re-found | 2026-09-17 |
| Pass 4 wave 5 (2026-09-17): 19 structural parts (the coinbase transaction fields, the scriptSig pieces, the output script framing) in all 11 renderings plus 114 window parts (16-byte windows of the block at stride 4, 32-byte at stride 8, 16-byte windows of the text) in the four core renderings, 10,908 entropies, 47 name formats, 52 paths; phase B pairs two entropies of the same part, as the author's "same Genesis field" requires | 133 parts, 10,908 entropies, 1,666,960,548 ordered pairs | same pipeline, `--wave 5` | 0 match | yes: revealed pair in the first, middle and last structural part, both phases, 6 of 6 re-found | 2026-09-17 |
| Pass 4 wave 6 (2026-09-18): eight further digest readings (MD4, MD2, Keccak-256 and Keccak-512 halves, SM3 halves) over 44 structural parts in all 11 renderings, plus every wave-4 entropy re-derived with uncompressed as well as compressed keys in the witness script | 6,868 entropies, 3,573,791,110 ordered pairs | same pipeline, `--wave 6` | 0 match | yes: revealed pair in the first, middle and last new-digest entropy, 3 of 3 re-found | 2026-09-18 |

## Open leads, ranked

1. **Buy the digest function, the one fact he has never refused** (needs a person; 10,000 sats).
   The category question above was sent on 2026-09-18 with 10,000 sats and refused: "Some part
   of the genesis block. The hints are meant to clarify the map, not hand you the route." The
   author answers about the form of the input, never about the input, so the remaining question
   worth paying for is the one about the function. Draft, 48 bytes:
   `128-bit digest: MD5? Or truncated SHA256? Which one?`
   Six passes spread their budget over 24 digest readings; an answer divides the next sweep by
   that factor whatever the part turns out to be. It is the last cheap fact I can name, and if
   it is refused too, the channel has given all it will give without a new idea.
2. **Enumerate the parts wave 5 did not reach** (hours on 8 cores, falling prior). Wave 5 took
   the coinbase transaction's fields, the script pieces and 114 windows of the block and the
   text at stride 4 and 8, and matched nothing. What is left on this line is windows at stride
   1, window lengths other than 16 and 32, and the fields as an explorer renders them in JSON.
   The cost grows and the prior falls with each of these.
3. **Watch the channel** (minutes). Re-read the escrow before any work: a new OP_RETURN from
   the author's change chain is a new constraint, a spend closes the puzzle. The author's
   current change output at 2026-09-17 is the change of
   `ed010443963e3601b35266a52108bd1b8dfa58e9e258a041098c05a474513fab`; it moves with every
   message, so follow the input chain of the last author transaction.
4. **The 50,000-sat public-key offer** (needs a person; not recommended). The keys would let a
   search test each candidate directly instead of pairing, which removes the smaller half of
   the cost: in this folder's runs, derivation takes longer than pairing. It buys about a
   factor of two, for five times the price of a question, and says nothing about the input.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | every OP_RETURN of the dialogue, verbatim, with txid, block and time |
| `data/genesis-block.hex` | the raw genesis block, 285 bytes, as served by any node or explorer |
| `data/on-chain-dialogue.json` | the 24 escrow transactions: sender attribution, amounts, decoded OP_RETURN, fetched 2026-09-12 |
| `analysis/tested.md` | the negatives ledger: passes 1 and 2 in full, with their exact scope |
| `analysis/leads.md` | full notes behind the ranked leads, with family sizes and the two killed passes |
| `tools/oracle.py` | candidate checker: two keys to 2-of-2 P2WSH, both orders, exact match; `--selftest` |
| `tools/candidates.py` | key generator for passes 1 and 2 (families A to G, labeled), witness insertion, targets file, CPU re-derivation of GPU hits |
| `tools/check_digest_model.py` | pass 4: the 2026-09-14 to 2026-09-17 model (128-bit digest entropy, name passphrase), waves 1 and 2, witness insertion, exact compare |

## Sources

- Announcement transaction, block 963,629, 2026-08-22: https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77
- Escrow address and full dialogue: https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj
- Galaxy Research, first public report, X, 2026-08-23: https://x.com/glxyresearch/status/2091349771952742566
- crypto.news, "Bitcoin puzzle hides wallet key in Genesis Block data", 2026-08-23: https://crypto.news/bitcoin-puzzle-hides-wallet-key-in-genesis-block-data/
- U.Today, 2026-08-23: https://u.today/satoshis-code-reopened-someone-just-deciphered-bitcoin-puzzle-into-genesis-block-data
- Blockmedia (Korean), 2026-08-23: https://www.blockmedia.co.kr/archives/1131026
- Genesis block, Bitcoin Wiki: https://en.bitcoin.it/wiki/Genesis_block

Credits: @BorisLoveDev (PR #21): the six 2026-09-05 bounded constructions and their scripts.
