BEGIN TRANSACTION;
CREATE TABLE recipes(id integer primary key, recipe text not null);
CREATE TABLE scope(id integer primary key, priority integer, scope_recipe_id integer, recipe_id integer);
CREATE TABLE vars(id integer primary key, var text, val text, recipe_id integer);

INSERT INTO "recipes" VALUES(NULL, 'bitbake.conf');
INSERT INTO "recipes" VALUES(NULL, 'base.bbclass');
INSERT INTO "recipes" VALUES(NULL, 'autotools.bbclass');
INSERT INTO "recipes" VALUES(NULL, 'a.bb');
INSERT INTO "recipes" VALUES(NULL, 'b.bb');

INSERT INTO "scope" VALUES(NULL, 2, 2, 2);
INSERT INTO "scope" VALUES(NULL, 1, 1, 2);

INSERT INTO "scope" VALUES(NULL, 3, 3, 3);
INSERT INTO "scope" VALUES(NULL, 2, 2, 3);
INSERT INTO "scope" VALUES(NULL, 1, 1, 3);

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
JOIN scope ON vars.recipe_id = scope.scope_recipe_id
JOIN recipes ON scope.recipe_id = recipes.id
WHERE vars.var = 'CC' AND recipes.recipe = 'base.bbclass'
ORDER BY scope.priority DESC
limit 1;

SELECT val FROM vars
JOIN scope ON vars.recipe_id = scope.scope_recipe_id
WHERE vars.var = 'CC' AND scope.recipe_id = 4
ORDER BY scope.priority DESC
limit 1;
