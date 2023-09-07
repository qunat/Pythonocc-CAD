// Created on: 1996-11-29
// Created by: Christophe LEYNADIER
// Copyright (c) 1996-1999 Matra Datavision
// Copyright (c) 1999-2014 OPEN CASCADE SAS
//
// This file is part of Open CASCADE Technology software library.
//
// This library is free software; you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License version 2.1 as published
// by the Free Software Foundation, with special exception defined in the file
// OCCT_LGPL_EXCEPTION.txt. Consult the file LICENSE_LGPL_21.txt included in OCCT
// distribution for complete text of the license and disclaimer of any warranty.
//
// Alternatively, this file may be used under the terms of Open CASCADE
// commercial license or contractual agreement.

#ifndef _FSD_CmpFile_HeaderFile
#define _FSD_CmpFile_HeaderFile

#include <FSD_File.hxx>
#include <Storage_BaseDriver.hxx>
#include <Storage_Error.hxx>
#include <Storage_OpenMode.hxx>
#include <Standard_Boolean.hxx>
#include <Standard_Integer.hxx>
#include <Standard_CString.hxx>
class TCollection_AsciiString;
class TCollection_ExtendedString;
class Storage_BaseDriver;

class FSD_CmpFile : public FSD_File
{
public:

  DEFINE_STANDARD_ALLOC


  Standard_EXPORT FSD_CmpFile();

  Standard_EXPORT Storage_Error Open(const TCollection_AsciiString& aName, const Storage_OpenMode aMode);

  Standard_EXPORT static Storage_Error IsGoodFileType(const TCollection_AsciiString& aName);

  Standard_EXPORT Storage_Error BeginWriteInfoSection();

  Standard_EXPORT Storage_Error BeginReadInfoSection();

  Standard_EXPORT void WritePersistentObjectHeader(const Standard_Integer aRef, const Standard_Integer aType);

  Standard_EXPORT void BeginWritePersistentObjectData();

  Standard_EXPORT void BeginWriteObjectData();

  Standard_EXPORT void EndWriteObjectData();

  Standard_EXPORT void EndWritePersistentObjectData();

  Standard_EXPORT void ReadPersistentObjectHeader(Standard_Integer& aRef, Standard_Integer& aType);

  Standard_EXPORT void BeginReadPersistentObjectData();

  Standard_EXPORT void BeginReadObjectData();

  Standard_EXPORT void EndReadObjectData();

  Standard_EXPORT void EndReadPersistentObjectData();

  Standard_EXPORT void Destroy();
  ~FSD_CmpFile()
  {
    Destroy();
  }

  Standard_EXPORT static Standard_CString MagicNumber();



protected:


  //! read from the current position to the end of line.
  Standard_EXPORT void ReadLine(TCollection_AsciiString& buffer);

  //! read extended chars (unicode) from the current position to the end of line.
  Standard_EXPORT void ReadExtendedLine(TCollection_ExtendedString& buffer);

  //! write from the current position to the end of line.
  Standard_EXPORT void WriteExtendedLine(const TCollection_ExtendedString& buffer);

  //! read from the first none space character position to the end of line.
  Standard_EXPORT void ReadString(TCollection_AsciiString& buffer);

};

#endif // _FSD_CmpFile_HeaderFile
