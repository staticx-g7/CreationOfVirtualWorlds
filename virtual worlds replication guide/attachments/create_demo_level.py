"""Build DemoWorld for VWClassDemo (UE 5.7+, verified API for 5.7.4).

Order matters: File -> New Level -> Empty Level, then SAVE AS /Game/Maps/DemoWorld
(so the save below has a target map), then run in the Output Log python tab:

    exec(open("/abs/path/create_demo_level.py").read())

Creates: Sun (8.0), realtime SkyLight (2.5), height fog, 2 km Ground plane,
PropSlot_00..07 cubes in a circle with BasicShapeMaterial, then saves.
5.7 API notes: no EditorLevelLibrary.get_level_actors, class is unreal.SkyLight,
components via get_component_by_class — see replication guide 14.
"""
import math
import unreal

sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
MAT = unreal.load_asset("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial")


def mesh_actor(path, loc, label, scale=(1.0, 1.0, 1.0)):
    a = sub.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc))
    a.set_actor_label(label)
    smc = a.get_component_by_class(unreal.StaticMeshComponent)
    smc.set_static_mesh(unreal.load_asset(path))
    if MAT:
        smc.set_material(0, MAT)
    a.set_actor_scale3d(unreal.Vector(*scale))
    return a


# Light: sun
sun = sub.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 2000))
sun.set_actor_label("Sun")
sun.set_actor_rotation(unreal.Rotator(pitch=-45.0, yaw=35.0, roll=0.0), False)
sun.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(8.0)

# SkyLight (realtime capture — no baked HDR needed)
sky = sub.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 500))
sky.set_actor_label("SkyLight")
skyc = sky.get_component_by_class(unreal.SkyLightComponent)
skyc.set_editor_property("real_time_capture", True)
skyc.set_intensity(2.5)

# Fog
fog = sub.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0, 0, 0))
fog.set_actor_label("HeightFog")

# Ground: /Engine plane (100 m) scaled 20x -> 2 km
mesh_actor("/Engine/BasicShapes/Plane.Plane", (0, 0, 0), "Ground", (20.0, 20.0, 1.0))

# 8 labelled prop slots in a ring, r = 8 m
for i in range(8):
    ang = math.radians(i * 45.0)
    mesh_actor("/Engine/BasicShapes/Cube.Cube",
               (math.cos(ang) * 800.0, math.sin(ang) * 800.0, 50.0),
               "PropSlot_%02d" % i)

# Save current (already-saved) level
try:
    ok = unreal.EditorLoadingAndSavingUtils.save_current_map(False)
except AttributeError:
    ok = unreal.EditorLevelLibrary.save_current_level()
print("DemoWorld built: sun + skylight + fog + ground + 8 PropSlots | saved:", ok)
