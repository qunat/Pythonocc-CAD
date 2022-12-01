SetFactory("OpenCASCADE");

    Mesh.CharacteristicLengthMin = 1;
    Mesh.CharacteristicLengthMax = 5;

    a() = ShapeFromFile("shape.brep");
    