# wiki_stats
Glean statistics from Wikipedia

### How many translations are available for personal page \<X\> ?

```tcsh
./wiki_count_languages.py https://sv.wikipedia.org/wiki/Jens_Johansson
Processing URL: https://sv.wikipedia.org/wiki/Jens_Johansson
Found Wikidata ID: Q182352
https://ar.wikipedia.org/wiki/ينس_يوهانسون
https://arz.wikipedia.org/wiki/ينس_يوهانسون
https://azb.wikipedia.org/wiki/ینس_یوهانسون
https://cs.wikipedia.org/wiki/Jens_Johansson
https://de.wikipedia.org/wiki/Jens_Johansson
https://el.wikipedia.org/wiki/Γιενς_Γιόχανσον
https://en.wikipedia.org/wiki/Jens_Johansson
https://es.wikipedia.org/wiki/Jens_Johansson
https://fi.wikipedia.org/wiki/Jens_Johansson
https://fr.wikipedia.org/wiki/Jens_Johansson
https://id.wikipedia.org/wiki/Jens_Johansson
https://it.wikipedia.org/wiki/Jens_Johansson
https://ja.wikipedia.org/wiki/イェンス・ヨハンソン
https://ka.wikipedia.org/wiki/იენს_იუჰანსონი
https://ko.wikipedia.org/wiki/옌스_요한손
https://no.wikipedia.org/wiki/Jens_Johansson
https://pl.wikipedia.org/wiki/Jens_Johansson
https://pt.wikipedia.org/wiki/Jens_Johansson
https://ru.wikipedia.org/wiki/Юханссон,_Йенс
https://simple.wikipedia.org/wiki/Jens_Johansson
https://sv.wikipedia.org/wiki/Jens_Johansson

Total distinct language pages: 21
```

### OK... well how many actual humans are there on Wiki anyway?

```tcsh
./wiki_count_humans.py
Total non-fictional persons (QIDs): 13461343
```

### Note Possible future metric erosion by the unwashed cloutlord hordes of the internet

Posting this 2026-06. [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law) would likely start applying to this metric, if it ever were to become some kind of common thing that people brag about.

![Very nice ... let's see Paul Allens wikipedia languages](https://i.kym-cdn.com/entries/icons/original/000/030/892/bateman.jpg)

_Very nice ... let's see Paul Allens wikipedia languages_



