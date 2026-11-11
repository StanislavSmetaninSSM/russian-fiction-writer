# Как писать художественную прозу на русском

Писательский скилл для работы над сценой, главой или романом. [Начните с выбора задачи](references/skills/notron-prose-examples/SKILL.md#как-пользоваться-писательскими-скиллами) или откройте [авторский практикум по прозе Нотрона](references/skills/notron-prose-examples/SKILL.md). В нём можно прочитать, как Люциан ждёт ответа братьев, как Найрена добивается от Керзена точного обещания и как одна правка местоимения меняет смысл всей реплики.

## Как передать скилл модели

**В чате** приложите [полную текстовую версию одним файлом](https://github.com/StanislavSmetaninSSM/russian-fiction-writer/releases/latest/download/SKILL.md), свою задачу и отрывок рукописи. В нём собраны оба авторских скилла, пять дополнительных скиллов и их справочные материалы. Попросите модель начать с таблицы и читать разделы по задаче. Например:

> Прочитай скилл и отредактируй разговор в этой сцене. Дочь хочет, чтобы отец остался. Он ей верит, но у него есть причина уйти. Сохрани его право отказать и слова, к которым она вернётся через две главы.

**Для агента с доступом к файлам** поместите папку репозитория целиком в его каталог скиллов под именем `russian-fiction-writer`. Например, из корня проекта с каталогом `.agents/skills`:

```sh
git clone https://github.com/StanislavSmetaninSSM/russian-fiction-writer.git .agents/skills/russian-fiction-writer
```

Точкой входа служит корневой [SKILL.md](SKILL.md). Сохраняйте структуру `references/`, чтобы агент мог читать русские разборы, полные руководства и справочники на диске. Интернет нужен для первоначального получения репозитория. Для работы с текстом достаточно чтения Markdown.

Если ваш агент выбирает скиллы по имени из общего каталога, можно зарегистрировать их по отдельности. Скопируйте все семь папок из `references/skills/` рядом друг с другом в каталог скиллов агента. У каждой есть собственный `SKILL.md`; ссылки из писательского скилла в практикум и к пяти дополнительным руководствам продолжат работать.

## Состав пакета

Корневой [SKILL.md](SKILL.md) связывает семь самостоятельных скиллов. Два из них — публичные редакции писательских скиллов «Хроник Нотрона».

| Авторский скилл | Для чего открыть |
|---|---|
| [notron-chronicle-writer](references/skills/notron-chronicle-writer/SKILL.md) | Спланировать главу, проверить канон и точку зрения, провести редактуру по секциям. Отдельно доступны [правила канона](references/skills/notron-chronicle-writer/references/canon-and-context.md), [авторский эталон](references/skills/notron-chronicle-writer/references/author-style-benchmark.md) и [порядок независимой вычитки](references/skills/notron-chronicle-writer/references/review-checklist.md). |
| [notron-prose-examples](references/skills/notron-prose-examples/SKILL.md) | Выбрать приём по задаче, прочитать отрывок и авторские правки «до/после», затем проверить на своей сцене, что услышал собеседник и что изменилось. |

Пять дополнительных скиллов включены целиком в тех редакциях, которые используются в Нотроне. В правой колонке указаны исходные версии для атрибуции. Для работы открывайте локальные файлы в левой колонке.

| Скилл в комплекте | Автор, исходная редакция и лицензия |
|---|---|
| [novel-writing](references/skills/novel-writing/SKILL.md) | wgwtest · [c57b5c6](https://github.com/wgwtest/novel-writing/tree/c57b5c6b35d30d692a06c7fe9cc030bd4ea7af14/novel-writing) · [MIT](references/skills/novel-writing/LICENSE) |
| [dialogue](references/skills/dialogue/SKILL.md) | J Wynia · [e02ec7e](https://github.com/jwynia/agent-skills/tree/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/creative/fiction/character/dialogue) · [MIT](references/skills/dialogue/LICENSE) |
| [prose-style](references/skills/prose-style/SKILL.md) | J Wynia · [e02ec7e](https://github.com/jwynia/agent-skills/tree/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/creative/fiction/craft/prose-style) · [MIT](references/skills/prose-style/LICENSE) |
| [novel-revision](references/skills/novel-revision/SKILL.md) | J Wynia · [e02ec7e](https://github.com/jwynia/agent-skills/tree/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/creative/fiction/structure/novel-revision) · [MIT](references/skills/novel-revision/LICENSE) |
| [cliche-transcendence](references/skills/cliche-transcendence/SKILL.md) | J Wynia · [e02ec7e](https://github.com/jwynia/agent-skills/tree/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/creative/fiction/craft/cliche-transcendence) · [MIT](references/skills/cliche-transcendence/LICENSE) |

Дополнительная проверка файлов рукописи из `novel-writing` использует Python 3. Англоязычные анализаторы лексики и ритма используют Deno. Для проверки клише скрипт лежит в `cliche-transcendence/scripts/orthogonality-check.ts`. В исходном руководстве также упоминается необязательная утилита `entropy.ts` из отдельного проекта `story-sense`. В этот набор она не входит.

При обновлении пакета файл для чата можно собрать из корня репозитория командой `python scripts/build_chat_edition.py ../SKILL.md`. Выберите свободный путь за пределами пакета. Скрипты помощников остаются в папочной версии.
