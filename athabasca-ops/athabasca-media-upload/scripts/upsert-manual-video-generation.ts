import { readFileSync } from "node:fs";
import { db } from "../../../src/server/db/client";
import { makeId } from "../../../src/server/db/ids";
import { mediaAssets, mediaGenerations } from "../../../src/server/db/schema";
import { eq } from "drizzle-orm";

function required(name: string): string {
  const value = process.env[name];
  if (!value?.trim()) throw new Error(`Missing required env var: ${name}`);
  return value.trim();
}

function optionalNumber(name: string): number | undefined {
  const value = process.env[name];
  if (!value?.trim()) return undefined;
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) throw new Error(`Invalid numeric env var ${name}: ${value}`);
  return parsed;
}

const assetId = required("ASSET_ID");
const promptPath = required("PROMPT_FILE");
const prompt = readFileSync(promptPath, "utf8");
const provider = process.env.PROVIDER?.trim() || "mitte.ai";
const model = process.env.MODEL?.trim() || "manual-video-generation";
const title = process.env.TITLE?.trim();
const provenanceNote = process.env.PROVENANCE_NOTE?.trim();
const projectSlug = process.env.PROJECT_SLUG?.trim();
const phaseTag = process.env.PHASE_TAG?.trim() || "clips";
const sceneTag = process.env.SCENE_TAG?.trim();
const group = process.env.GROUP?.trim();
const durationMs = optionalNumber("DURATION_MS");
const requestedSeconds = optionalNumber("DURATION_SECONDS_REQUESTED");
const shotCount = optionalNumber("SHOT_COUNT");
const secondsPerShot = optionalNumber("SECONDS_PER_SHOT");
const noMusic = process.env.NO_MUSIC === "true" ? true : process.env.NO_MUSIC === "false" ? false : undefined;
const transition = process.env.TRANSITION?.trim();
const now = new Date().toISOString();

const asset = await db.query.mediaAssets.findFirst({ where: eq(mediaAssets.id, assetId) });
if (!asset) throw new Error(`Media asset not found: ${assetId}`);

let metadata: Record<string, unknown> = {};
try {
  metadata = JSON.parse(asset.metadataJson || "{}");
} catch {
  metadata = {};
}

const parameters: Record<string, unknown> = {
  ...(typeof metadata.parameters === "object" && metadata.parameters ? metadata.parameters as Record<string, unknown> : {}),
};
if (requestedSeconds !== undefined) parameters.durationSecondsRequested = requestedSeconds;
if (shotCount !== undefined) parameters.shotCount = shotCount;
if (secondsPerShot !== undefined) parameters.secondsPerShot = secondsPerShot;
if (transition) parameters.transition = transition;
if (noMusic !== undefined) parameters.noMusic = noMusic;

const mergedMetadata = {
  ...metadata,
  workflow: "manual-video-generation-upload",
  ...(projectSlug ? { projectSlug } : {}),
  phaseTag,
  provider,
  generator: provider,
  model,
  promptStatus: "provided-by-user",
  promptSource: "user-supplied prompt",
  promptProvidedAt: now,
  documentMutation: "none",
  ...(sceneTag ? { sceneTag } : {}),
  ...(group ? { group } : {}),
  ...(Object.keys(parameters).length ? { parameters } : {}),
  prompt,
};

await db.update(mediaAssets)
  .set({
    ...(title ? { title } : {}),
    ...(provenanceNote ? { provenanceNote } : {}),
    metadataJson: JSON.stringify(mergedMetadata),
    updatedAt: now,
  })
  .where(eq(mediaAssets.id, assetId));

const parametersJson = JSON.stringify({
  workflow: "manual-video-generation-upload",
  ...(projectSlug ? { projectSlug } : {}),
  phaseTag,
  provider,
  generator: provider,
  model,
  promptSource: "user-supplied prompt",
  ...(sceneTag ? { sceneTag } : {}),
  ...(group ? { group } : {}),
  ...parameters,
  documentMutation: "none",
});

const existingGeneration = await db.query.mediaGenerations.findFirst({ where: eq(mediaGenerations.assetId, assetId) });
if (existingGeneration) {
  await db.update(mediaGenerations)
    .set({
      provider,
      model,
      prompt,
      negativePrompt: null,
      ...(durationMs !== undefined ? { durationMs } : {}),
      parametersJson,
      updatedAt: now,
    })
    .where(eq(mediaGenerations.assetId, assetId));
} else {
  await db.insert(mediaGenerations).values({
    id: makeId("gen"),
    assetId,
    provider,
    model,
    prompt,
    negativePrompt: null,
    durationMs: durationMs ?? null,
    parametersJson,
    createdAt: now,
    updatedAt: now,
  });
}

const after = await db.query.mediaGenerations.findFirst({ where: eq(mediaGenerations.assetId, assetId) });
console.log(JSON.stringify({
  ok: true,
  assetId,
  generationId: after?.id,
  provider: after?.provider,
  model: after?.model,
  promptLength: after?.prompt.length,
  promptStarts: after?.prompt.slice(0, 120),
}, null, 2));
