# Leads (full notes)

The "Open leads, ranked" section of the folder's `README.md` shows the ranked list; this file
carries the full notes behind each entry. Order leads by cost to test, then by expected
value.

Notation: T is the 69-byte coinbase text `The Times 03/Jan/2009 Chancellor on brink of second
bailout for banks`, J the 47-byte headline `Chancellor on brink of second bailout for banks`,
S the full 77-byte scriptSig, and G the set of genesis integers {nonce 2083236893, time
1231006505, bits 486604799, version 1, height 0, 2, 3, 2009, 50}, all under 2^31 and so valid
as hardened BIP32 indexes.

## 1. Read the author's next answer (open)

- **Cost**: minutes, no payment. Player 5 already paid 3,000 sats for the question.
- **What it is**: at 2026-09-17 10:44 UTC player 5 asked "Digest input: typed text, raw block
  bytes, a file, or something else?" and it is unanswered at 15:30 UTC. Every paid question so
  far was answered in 1 to 10 hours.
- **Why it ranks first**: pass 4 tested 73 readings of "genesis data" under 18 digest functions
  and matched nothing, so the input is not an obvious one. This answer names it for free.
- **What would confirm it**: a new OP_RETURN spending the author's current change output,
  `bc1qnsk37lnc9unj4d4jjq5j3nh5u88dvfltv9r7xr`.
- **What would kill it**: the author stops answering, or someone spends the escrow.
- **Status**: open

## 2. Ask for the digest function and its input (open)

- **Cost**: needs a person; 5,000 to 10,000 sats bought each September answer within hours.
- **What it is**: one OP_RETURN of at most 80 bytes with a payment to the escrow. Draft,
  76 bytes: `Digest fn: MD5, or truncated SHA-256? Digest taken over which genesis bytes?`
- **Why it ranks here**: the author said "a 128-bit digest" without naming the function. Pass 4
  spent 6.44e9 pairs on the product of 18 functions and 73 inputs; one answer collapses it.
- **What would confirm it**: any answer, checked with the oracle in seconds.
- **What would kill it**: the author stops answering, or a spend of the escrow.
- **Status**: open

## 3. Ask the author one precise question on chain (done, by a reader)

- **Cost**: needs a person; about 5,000 to 10,000 sats plus fees; answer within hours (every
  paid question so far was answered in 1 to 10 hours)
- **What it is**: a transaction with one output to the escrow (or to the author's current
  change address, which the author then relays) and one OP_RETURN of at most 80 bytes with
  the question. Draft, 79 bytes:
  `Root = BIP32 seed from coinbase text directly? account = genesis nonce?`
  Shorter variant, 55 bytes: `Is root seeded by the 69-byte coinbase text, no BIP39?`
- **Why it ranks here**: passes 1 and 2 (below, both killed) exhausted the plain and the
  library-specific readings of "root" and "genesis_data"; the author sells hints and has
  answered every one; the two most useful hints cost 3,000 and 3,500 sats. One answer
  collapses the space to a few dozen candidates. The question I would send, 78 bytes:
  `Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account?`
- **What would confirm it**: any answer, checked against the oracle in seconds.
- **What would kill it**: the author stops answering (last answer 2026-08-28 23:50 UTC), or a
  spend of the escrow by someone else.
- **Status**: done, by a reader. On 2026-09-10 a player sent the 78-byte question above
  with 10,000 sats and got, within the hour: "root = the master key derived from the BIP39
  seed; genesis_data = some data from the genesis block used as the BIP48 account number."
  On 2026-09-11 the same player sent the second draft, "BIP39 entropy: genesis bytes/puzzle
  text/img/other? words 12/24? passphrase Y/N?", and got: "BIP39: 12 words; Passphrase: Y;
  Entropy: The data needed to solve it is publicly available in the genesis block." The
  model is now: 12-word mnemonic, 128-bit entropy taken from genesis data, a non-empty
  passphrase the author has not described, BIP48 with a genesis value as account, two keys
  derived independently from the same field. The next question to buy is about the
  passphrase (README, lead 2); the next computation is pass 3 (README, lead 1).

## 4. Watch the channel

- **Cost**: minutes
- **What it is**: before any work, re-read the escrow's transactions on an explorer. A new
  OP_RETURN spending the author's latest change output is a new constraint; a spend of the
  escrow ends the puzzle. The author's current change address is
  `bc1qw720l9e6g4a675vfraghzm93gvyw8s2fjgtdxy` (unspent on 2026-09-12); it
  changes with every message, so follow the chain of inputs from the last author
  transaction rather than this fixed address.
- **Why it ranks here**: zero cost, and every hint so far reduced the space more than any
  computation could.
- **What would confirm it**: a new author message.
- **What would kill it**: a spend of the escrow.
- **Status**: open

## 5. Pass 2: library-specific root constructions (killed 2026-08-29)

- **Cost**: minutes (about 165,000 more keys on the CPU, then about 90 s on one GPU
  paired with the pass 1 set)
- **What it is**: the root constructions pass 1 did not model, along the same 214 paths:
  - E, hashed roots: SHA-256, double SHA-256, hash160 and SHA-512 of each text (T, J, S and
    their case forms) used as a raw private key, as a BIP32 seed and as BIP39 entropy. The
    author said "no hash", but the cost is a few thousand keys.
  - F, raw extended key: 32 key bytes and 32 chain-code bytes taken directly from the text
    (`T[:32]` with `T[32:64]`, `S[:32]` with `S[32:64]`, the reversed forms, and the two
    halves swapped), which is a "no hash, no backup" reading of a 64-byte master key.
  - G, raw private key with a zero chain code, the way some libraries import a bare 32-byte
    key into an HD wallet object, for every 16 to 32-byte window of T (padded as in family A).
- **Why it ranks here**: cheap, and it is the only remaining mechanical reading of "root ->
  multisig -> mainnet -> genesis_data -> script_type" that keeps "genesis_data" at the account
  level; it ranks below lead 1 because a single answer from the author is worth more than any
  of these guesses.
- **What would confirm it**: a MATCH from the engine, re-derived on the CPU.
- **What would kill it**: 0 match with the witness pair re-found at head, middle and tail.
- **Result, 2026-08-29**: run with `tools/candidates.py --pass 2`: 16,548 E keys, 2,996 F
  keys and 145,306 G keys before deduplication (70 hashed integers, 77 hashed seeds, 14 raw
  extended keys, 680 zero-chain-code roots, 214 paths), union with pass 1 = 611,008 distinct
  keys, 373,338,108,196 ordered pairs on the GPU, 0 match, witness pair re-found in all 9
  combinations, 89 s. Full scope in `tested.md`.
- **Status**: killed

## 6. Pass 1: bounded first pass over the coinbase text (killed 2026-08-29)

- **Cost**: minutes
- **What it is**: the literal readings of the two 2026-08-28 hints, enumerated. Four families:
  - A, raw private keys: every window of 1 to 32 bytes of T, J and S, read as a big-endian
    integer, as a little-endian integer, left-padded and right-padded to 32 bytes, with
    compressed and uncompressed public keys. About 15,000 distinct keys, 1.1e8 pairs, two
    key orders each, about 4 minutes at 1,200,000 pairs/s.
  - B, BIP32 root plus BIP48 path: seed in {T, J, S, T[:32], T[32:], J[:32], every 16 and
    32-byte window}, paths `m/48'/0'/a'/s'/0/i` with a in G, s in {0', 1', 2'}, i in {0, 1},
    plus `m`, `m/0`, `m/0/0`, `m/44'/0'/0'/0/0`, `m/84'/0'/0'/0/0`. About 60 seeds times 70
    paths, 4,000 keys, under a minute.
  - C, BIP39 entropy: windows of T, J and S of 16, 20, 24, 28 and 32 bytes as entropy, the
    resulting mnemonic with an empty passphrase and with T as passphrase, then the paths of
    B. About 35,000 keys, 6e8 pairs, about 10 minutes.
  - D, other fields: merkle root, block hash, public key and header, raw, byte-reversed and
    truncated, as raw keys, as seeds and as entropy, with accounts in G. About 500 keys,
    seconds.
  Pairs are also taken across families (A with B, B with C) while the total stays under 1e9
  hashes. Free filters: a raw key must lie in [1, n-1] (short windows right-padded overflow
  and are dropped); BIP39 entropy must be 16 to 32 bytes in steps of 4.
- **Why it ranks here**: cheapest possible test of what the author literally said. "Maybe
  both" to "32 bytes or smaller" fits one key on T[:32] (`The Times 03/Jan/2009 Chancellor`,
  exactly 32 bytes) and one on a shorter slice; "root -> multisig -> mainnet -> genesis_data
  -> script_type" is the BIP48 level order with a genesis value in the account slot.
- **What would confirm it**: a MATCH from `tools/oracle.py`.
- **What would kill it**: 0 match with the witness re-found at head, middle and tail of each
  family.
- **Result, 2026-08-29**: run as described, with the four families merged into one key set of
  447,916 distinct public keys (the sizes above were estimates; the exact counts are 36,816
  raw integers, 1,370 BIP32 seeds and 2,730 BIP39 seeds along 214 paths, deduplicated) and
  every ordered pair checked on the GPU: 200,634,118,084 pairs, 0 match, the witness pair
  re-found in all 9 head/middle/tail combinations, 103 s. Full scope in `tested.md`.
- **Status**: killed (the literal readings are closed; the puzzle is not)

## 7. Pass 4: the digest model (killed 2026-09-17)

- **Cost**: 26 minutes on 8 CPU cores, no GPU
- **What it is**: the model the author described between 2026-09-14 and 2026-09-17. Entropy is
  a 128-bit digest of genesis data, not a raw window; the 12 words are generated from it; the
  passphrase is a name, the name of whoever received the first transaction, in a format the
  author says has to be brute-forced; the path is BIP48 with a genesis value as account.
  Wave 1 pairs two keys from one seed; wave 2 pairs two keys from two different digests at the
  same path, which is the ordinary two-cosigner setup. Both names are covered: Hal Finney, who
  received the first Bitcoin payment in block 170, and Satoshi Nakamoto, who received the
  coinbase of the genesis block.
- **Result, 2026-09-17**: 1,278 digest entropies (18 digest readings over 73 genesis inputs),
  47 name formats, 13 genesis accounts, script types 0'/1'/2'. Wave 1: 9,370,296 keys,
  1,452,484,146 ordered pairs, 0 match, witness 141 of 141. Wave 2: 3,904,290 keys,
  4,986,775,560 ordered pairs, 0 match, witness 195 of 195. Reproduce with
  `tools/check_digest_model.py --wave 1` and `--wave 2`.
- **What it leaves open**: the digest input (the subject of lead 1), the name format beyond the
  47 tested, a digest function outside the 18, and a mixed pair (two passphrases or two paths
  across the two cosigners).
- **Status**: killed for the 73 listed inputs; the model itself stands
