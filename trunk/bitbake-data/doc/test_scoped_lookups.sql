BEGIN TRANSACTION;
CREATE TABLE files(key integer primary key, file text not null);
CREATE TABLE scope(key integer primary key, priority integer, scope integer, file integer);
CREATE TABLE vars(key integer primary key, var text, val text, file integer);

INSERT INTO "files" VALUES(NULL, 'bitbake.conf');
INSERT INTO "files" VALUES(NULL, 'base.bbclass');
INSERT INTO "files" VALUES(NULL, 'autotools.bbclass');
INSERT INTO "files" VALUES(NULL, 'a.bb');
INSERT INTO "files" VALUES(NULL, 'b.bb');

INSERT INTO "scope" VALUES(NULL, 3, 4, 4);
INSERT INTO "scope" VALUES(NULL, 2, 2, 4);
INSERT INTO "scope" VALUES(NULL, 1, 1, 4);

INSERT INTO "scope" VALUES(NULL, 1, 1, 5);
INSERT INTO "scope" VALUES(NULL, 2, 2, 5);
INSERT INTO "scope" VALUES(NULL, 3, 3, 5);
INSERT INTO "scope" VALUES(NULL, 4, 5, 5);

INSERT INTO "vars" VALUES(NULL, 'CC', 'bitbake.conf_cc', 1);
INSERT INTO "vars" VALUES(NULL, 'CC', 'base.bbclass_cc', 2);
INSERT INTO "vars" VALUES(NULL, 'CC', 'autotools.bbclass_cc', 3);
INSERT INTO "vars" VALUES(NULL, 'CC', 'a.bb_cc', 4);
INSERT INTO "vars" VALUES(NULL, 'CC', 'b.bb_cc', 5);

COMMIT;

SELECT val FROM vars
JOIN scope ON vars.file = scope.scope
WHERE var = 'CC' AND scope.file = 5
ORDER BY scope.priority DESC
limit 1;
